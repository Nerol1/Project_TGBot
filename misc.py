from aiogram.types import Message
from aiogram.enums import ChatAction
from datetime import datetime


def on_start():
    time_now = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    print(f'Bot is started at {time_now}')


def on_shutdown():
    time_now = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    print(f'Bot is down at {time_now}')


async def bot_thinking(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )