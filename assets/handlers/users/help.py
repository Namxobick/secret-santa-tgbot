import aiogram
from loguru import logger

from assets.secret_santa_loader import dispatcher
from assets.utils.misc import rate_limit


@rate_limit(limit=2, key='/help')
@dispatcher.message_handler(text='/help')
async def command_help(message: aiogram.types.Message):
    logger.info('{0} called the start command'.format(
        message.from_user.full_name,
    ))
    multiline = """
    Доступные команды:
    /create_lobby - создать новую комнату
    /join_lobby - присоединиться к существующей комнате
    /my_lobbies - узнать комнаты в которых ты состоишь
    """
    await message.answer(multiline)
    logger.info('{0} received a response from the start command'.format(
        message.from_user.full_name,
    ))
