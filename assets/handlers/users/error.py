import aiogram
from loguru import logger

from assets.secret_santa_loader import dispatcher


@dispatcher.message_handler()
async def command_error(message: aiogram.types.Message):
    logger.info('{0} called a non-existent command'.format(
        message.from_user.full_name,
    ))
    await message.answer('Команда {0} не существует!'.format(
        message.text,
    ))
    log_text = '{0} received a response that the command {1} does not exist'
    logger.info(log_text.format(
        message.from_user.full_name,
        message.text,
    ))
