import aiogram

from assets.middlewares.throttling import ThrottlingMiddleware


def setup(dispatcher: aiogram.Dispatcher):
    dispatcher.middleware.setup(ThrottlingMiddleware())
