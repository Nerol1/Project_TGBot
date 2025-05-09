from aiogram import Router

from .command import command_router
from .callback_handlers import callback_router
from .message_handler import message_router


main_router = Router()
main_router.include_routers(
    message_router,
    command_router,
    callback_router,
)

__all__ = [
    'main_router',
]