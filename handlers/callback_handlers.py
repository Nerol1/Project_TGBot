from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from openai.types.beta.threads.runs import ToolCallDeltaObject

from classes import gpt_client
from classes.resource import Resource, Button
from classes.chat_gpt import GPTMessage
from classes.enums import GPTRole
from keyboards.callback_data import CelebrityData, QuizData, LangData
from .handlers_state import CelebrityTalk, Quiz, Translate, Tutor
from keyboards import kb_reply, ikb_quiz_select_topic, ikb_tutor_next, kb_tutor, ikb_language
from .command import com_start

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
    photo = Resource(callback_data.file_name).photo
    button_name = Button(callback_data.file_name).name
    await callback.answer(
        text=f'С тобой говорит {button_name}',
    )
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption='Задайте свой вопрос:',
    )
    request_message = GPTMessage(callback_data.file_name)
    await state.set_state(CelebrityTalk.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo})



@callback_router.callback_query(LangData.filter(F.button == 'change_language'))
async def change_lang_callbacks(callback: CallbackQuery, callback_data: LangData, bot: Bot, state: FSMContext):
    command_type = callback_data.command_type
    resource = Resource(command_type)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        **resource.as_kwargs(),
        reply_markup=ikb_language(command_type),
    )




@callback_router.callback_query(LangData.filter(F.button == 'select_language'))
async def select_lang_callbacks(callback: CallbackQuery, callback_data: LangData, bot: Bot, state: FSMContext):
    command_type = callback_data.command_type
    photo = Resource(command_type).photo
    language_name = callback_data.lang_name
    await callback.answer(
        text=f'Выбран язык: {language_name}',
    )
    request_message = GPTMessage(command_type)
    if command_type == 'translate':
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=photo,
            caption='Напишите сообщение для перевода:',
        )
        await state.set_state(Translate.wait_for_answer)
    else:
        request_message.update(GPTRole.SYSTEM, f'Дай случайное слово на {callback_data.lang_name}')
        response = await gpt_client.request(request_message)
        new_word = response.split(" -> ")[0]
        request_message.add_new_word(new_word)
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=photo,
            caption=response,
            reply_markup=ikb_tutor_next(callback_data),
        )
        await state.set_state(Tutor.wait_for_word)
    await state.set_data({'messages': request_message, 'photo': photo, 'callback': callback_data})


@callback_router.callback_query(LangData.filter(F.button == 'next_word'))
async def tutor_next_word(callback: CallbackQuery, callback_data: LangData, state: FSMContext):
    data: dict[str, GPTMessage | str | LangData] = await state.get_data()
    photo = data['photo']
    request_message = data['messages']
    response = await gpt_client.request(request_message)
    new_word = response.split(" -> ")[0]
    request_message.add_new_word(new_word)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=response,
        reply_markup=ikb_tutor_next(callback_data),
    )
    await state.set_state(Tutor.wait_for_word)
    await state.set_data({'messages': request_message, 'photo': photo, 'callback': callback_data})


@callback_router.callback_query(LangData.filter(F.button == 'tutor_practice'))
async def tutor_practice(callback: CallbackQuery, callback_data: LangData, state: FSMContext):
    data: dict[str, GPTMessage | str | LangData] = await state.get_data()
    await callback.answer(
        text=f'Начинаем тренировку!',
    )
    await state.set_state(Tutor.wait_for_answer)
    word = data['messages'].get_next_word()
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=f'Напиши мне перевод слова {word} на русский язык:',
        reply_markup=kb_tutor(),
    )
    await state.set_data({'messages': data['messages'], 'photo': data['photo'], 'score': 0, 'word': word, 'callback': callback_data})




@callback_router.callback_query(QuizData.filter(F.button == 'change_topic'))
async def quiz_change_topic(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data: dict[str, GPTMessage | str | QuizData] = await state.get_data()
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=data['photo'],
        caption=f'Меняем тему!!',
        reply_markup=ikb_quiz_select_topic(),
    )


@callback_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def quiz_new_topic(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
    photo = Resource('quiz').photo
    await callback.answer(
        text=f'Вы выбрали тему {callback_data.topic_name}!',
    )
    request_message = GPTMessage('quiz')
    request_message.update(GPTRole.USER, callback_data.topic)
    response = await gpt_client.request(request_message)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=response,
    )
    await state.set_state(Quiz.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo, 'score': 0, 'callback': callback_data})


@callback_router.callback_query(QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data: dict[str, GPTMessage | str | QuizData] = await state.get_data()
    data['messages'].update(GPTRole.USER, 'quiz_more')
    response = await gpt_client.request(data['messages'])
    data['messages'].update(GPTRole.ASSISTANT, response)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=data['photo'],
        caption=response,
    )
    topic = data['callback'].topic_name
    await callback.answer(
        text=f'Продолжаем тему {topic}'
    )
    await state.update_data(data)

@callback_router.callback_query(QuizData.filter(F.button == 'finish_quiz'))
@callback_router.callback_query(LangData.filter(F.button == 'finish_tutor'))
async def return_to_start(callback: CallbackQuery, callback_data: QuizData|LangData, state: FSMContext):
    resource = Resource('main')
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
        '/translate',
        '/tutor'
    ]
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        **resource.as_kwargs(),
        reply_markup=kb_reply(buttons),
    )
    await state.clear()

