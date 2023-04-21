from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_admin_lobby_menu = InlineKeyboardMarkup(row_width=2,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text='Распределить',
                                                        callback_data='distribute',
                                                    ),
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text='Одаряемый',
                                                        callback_data='gifted',
                                                    ),
                                                    InlineKeyboardButton(
                                                        text='Участники',
                                                        callback_data='players',
                                                    ),
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text='Удалить комнату',
                                                        callback_data='delete',
                                                    ),
                                                ],
                                            ])
