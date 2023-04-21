import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from assets.data import config

parse_mode = aiogram.types.ParseMode.HTML
bot = aiogram.Bot(token=config.BOT_TOKEN, parse_mode=parse_mode)
storage = MemoryStorage()
dispatcher = aiogram.Dispatcher(bot, storage=storage)
