import aiogram
from loguru import logger

from assets.data.config import admins_id


async def on_startup_notify(dispatcher: aiogram.Dispatcher):
    for admin in admins_id:
        try:
            text = 'Bot is running'
            await dispatcher.bot.send_message(chat_id=admin, text=text)
        except Exception as ex:
            logger.exception('Bot could not inform the admin with id ={0} {1}'.format(
                admin,
                str(ex),
            ))
