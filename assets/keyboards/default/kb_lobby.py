import aiogram


def get_reply_markup(lobbies: list):
    return aiogram.types.ReplyKeyboardMarkup(
        keyboard=[
            [aiogram.types.KeyboardButton(text='{0}'.format(
                lobby[0],
            ))] for lobby in lobbies
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
