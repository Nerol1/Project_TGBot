from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.resource import Button, Buttons
from .callback_data import CelebrityData, QuizData, LangData
from classes.enums import Languages


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


def ikb_language():
    keyboard = InlineKeyboardBuilder()
    for language in Languages:
        button = Button(language.name, language.value)
        keyboard.button(
            text=button.name,
            callback_data=LangData(
                button='select_language',
                language=button.callback,
                lang_name=button.name,
            )

        )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_translate(current_language: LangData):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('change_language', 'Сменить язык'),
        Button('finish_translate', 'Закончить'),
    ]
    for button in buttons:
        keyboard.button(
            text=button.name,
            callback_data=LangData(
                button=button.callback,
                language=current_language.language,
                lang_name=current_language.lang_name,
            )
        )
    keyboard.adjust(2, 1)
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