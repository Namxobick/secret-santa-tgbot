from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb_lobby_menu = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
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
                                                  text='Выйти',
                                                  callback_data='leave',
                                              ),
                                          ],
                                      ])
