import aiogram

kb_menu = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [
            aiogram.types.KeyboardButton(text='/create_lobby'),
            aiogram.types.KeyboardButton(text='/join_lobby'),
        ],
        [
            aiogram.types.KeyboardButton(text='/my_lobbies'),
        ],
        [
            aiogram.types.KeyboardButton(text='/help'),
        ],
    ],
    resize_keyboard=True,
)
