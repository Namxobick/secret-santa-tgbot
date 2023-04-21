import aiogram
from loguru import logger

from assets.keyboards.default import kb_menu
from assets.secret_santa_loader import dispatcher
from assets.utils.misc import rate_limit


@rate_limit(limit=2, key='/start')
@dispatcher.message_handler(text='/start')
async def command_start(message: aiogram.types.Message):
    logger.info('{0} called the start command'.format(
        message.from_user.full_name,
    ))
    await message.answer(
        'Привет {0}!'.format(message.from_user.full_name),
        reply_markup=kb_menu,
    )
    logger.info('{0} received a response from the start command'.format(
        message.from_user.full_name,
    ))
