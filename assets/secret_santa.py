from loguru import logger

from assets import middlewares
from assets.utils.notify_admins import on_startup_notify
from assets.utils.set_bot_commands import set_default_command


async def on_startup(dispatcher):
    middlewares.setup(dispatcher)
    logger.info('Bot is running')
    await on_startup_notify(dispatcher)
    logger.info('Bot informed admins about the start')
    await set_default_command(dispatcher)
