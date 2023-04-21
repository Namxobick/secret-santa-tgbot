import aiogram
from aiogram.dispatcher.filters import Command
from loguru import logger

from assets.keyboards.default import kb_menu
from assets.secret_santa_loader import dispatcher
from assets.utils.misc import rate_limit


@rate_limit(limit=2, key='/menu')
@dispatcher.message_handler(Command('menu'))
async def menu(message: aiogram.types.Message):
    logger.info('{0} called the menu command'.format(
        message.from_user.full_name,
    ))
    await message.answer('Выбери команду из меню ниже', reply_markup=kb_menu)
    logger.info('{0} received a response from the menu command'.format(
        message.from_user.full_name,
    ))
