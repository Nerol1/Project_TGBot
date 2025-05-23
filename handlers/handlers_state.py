from aiogram.fsm.state import State, StatesGroup


class ChatGPTRequests(StatesGroup):
    wait_for_request = State()


class CelebrityTalk(StatesGroup):
    wait_for_answer = State()


class Quiz(StatesGroup):
    wait_for_answer = State()

class Translate(StatesGroup):
    wait_for_answer = State()

class Tutor(StatesGroup):
    wait_for_word = State()
    wait_for_answer = State()