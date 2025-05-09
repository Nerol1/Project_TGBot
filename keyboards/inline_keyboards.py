from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.resource import Button, Buttons
from .callback_data import CelebrityData, QuizData


def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    buttons = Buttons()
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=CelebrityData(
                button='select_celebrity',
                file_name=button.callback,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_select_topic():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('quiz_prog', 'Язык Python'),
        Button('quiz_math', 'Математика'),
        Button('quiz_biology', 'Биология'),

    ]
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=QuizData(
                button='select_topic',
                topic=button.callback,
                topic_name=button.name,
            )

        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_next(current_topic: QuizData):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('next_question', 'Дальше'),
        Button('change_topic', 'Сменить тему'),
        Button('finish_quiz', 'Закончить'),

    ]
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=QuizData(
                button=button.callback,
                topic=current_topic.topic,
                topic_name=current_topic.topic_name
            )
        )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()