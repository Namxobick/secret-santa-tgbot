from aiogram import executor
from loguru import logger

from assets.handlers import dispatcher
from assets.secret_santa import on_startup


def main():
    """Main method. Entry point."""
    try:
        executor.start_polling(dispatcher, on_startup=on_startup)
    except Exception as ex:
        logger.critical('You have done something wrong! {0}'.format(str(ex)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.critical('Shutting down, bye!')
