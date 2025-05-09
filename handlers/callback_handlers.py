from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from classes.resource import Resource, Button
from classes.chat_gpt import GPTMessage
from classes.enums import GPTRole
from keyboards.callback_data import CelebrityData, QuizData
from .handlers_state import CelebrityTalk, Quiz
from keyboards import kb_reply, ikb_quiz_select_topic

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
async def celebrity_callbacks(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
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
async def quiz_exit(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
    ]

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=f'Завершаем квиз!',
        reply_markup=kb_reply(buttons),
    )
    await callback.answer(
        text=f'Завершаем квиз!',
    )
    await state.clear()
