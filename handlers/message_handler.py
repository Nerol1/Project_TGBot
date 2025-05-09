from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .handlers_state import CelebrityTalk, ChatGPTRequests, Quiz, Translate

from classes import gpt_client
from classes.resource import Resource
from classes.chat_gpt import GPTMessage, GPTRole
from keyboards import kb_end_talk, ikb_quiz_next, kb_translate, ikb_language
from keyboards.callback_data import QuizData
from .command import com_start, com_translate
from misc import bot_thinking

message_router = Router()


@message_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
    await state.clear()
    await com_start(message)

@message_router.message(Translate.wait_for_answer, F.text == 'Закончить!')
async def end_translate_handler(message: Message, state: FSMContext):
    await state.clear()
    await com_start(message)


@message_router.message(Translate.wait_for_answer, F.text == 'Сменить язык')
async def end_translate_handler(message: Message, state: FSMContext):
    await com_translate(message)



@message_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    gpt_message = GPTMessage('gpt')
    gpt_message.update(GPTRole.USER, message.text)
    gpt_response = await gpt_client.request(gpt_message)
    photo = Resource('gpt').photo
    await message.answer_photo(
        photo=photo,
        caption=gpt_response,
    )
    await state.clear()


@message_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    data: dict[str, GPTMessage | str] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=kb_end_talk(),
    )
    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)

@message_router.message(Translate.wait_for_answer)
async def translate_handler(message: Message, state: FSMContext):
    await bot_thinking(message)
    data: dict[str, GPTMessage | str] = await state.get_data()
    current_language = data['callback'].language
    data['messages'].update(GPTRole.USER, f'{current_language}^{message.text}^')
    response = await gpt_client.request(data['messages'])
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=kb_translate(),
    )
    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.update_data(data)


@message_router.message(Quiz.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
    data: dict[str, GPTMessage | str | QuizData] = await state.get_data()
    data['messages'].update(GPTRole.USER, message.text)
    response = await gpt_client.request(data['messages'])
    if response == 'Правильно!':
        data['score'] += 1
    data['messages'].update(GPTRole.ASSISTANT, response)
    score = data['score']
    photo = Resource('quiz').photo
    await message.answer_photo(
        photo=photo,
        caption=f'Ваш счет: {score}\n{response}',
        reply_markup=ikb_quiz_next(data['callback']),
    )
    await state.update_data(data)