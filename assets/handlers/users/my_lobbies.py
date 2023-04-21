import aiogram
from aiogram.types import CallbackQuery
from loguru import logger

from assets.keyboards.default import get_reply_markup, kb_menu
from assets.keyboards.inline import ikb_admin_lobby_menu, ikb_lobby_menu
from assets.secret_santa_loader import dispatcher
from assets.states import ViewLobbyStates
from assets.storage.lobbies import Lobbies
from assets.utils.misc import rate_limit

lobbies = Lobbies.get_instance()


@rate_limit(limit=2, key='/my_lobby')
@dispatcher.message_handler(text='/my_lobbies')
async def command_my_lobbies(message: aiogram.types.Message):
    logger.info('{0} called the my_lobby command'.format(
        message.from_user.full_name,
    ))
    user_lobbies = lobbies.get_user_lobbies(message.from_user.id)
    if not user_lobbies:
        answer_text = 'Вы ещё не состоите не в одной из комнат'
        reply_markup = None
    else:
        answer_text = 'Ваши комнаты: \n'
        for user_lobby in user_lobbies:
            answer_text += 'Название: "{0}". Ваша в ней роль: {1}\n'.format(
                user_lobby[0],
                user_lobby[1],
            )
        answer_text += 'Выберите нужную комнату в меню ниже или напишите {название комнаты}'
        reply_markup = get_reply_markup(user_lobbies)

    await message.answer(answer_text, reply_markup=reply_markup)
    logger.info('{0} received a response from the my_lobby command'.format(
        message.from_user.full_name,
    ))
    if user_lobbies:
        await ViewLobbyStates.lobby.set()


@dispatcher.message_handler(state=ViewLobbyStates.lobby)
async def state_lobby(
    message: aiogram.types.Message,
    state: aiogram.dispatcher.FSMContext,
):
    logger.info('{0} chooses the lobby'.format(
        message.from_user.full_name,
    ))
    user_lobby = lobbies.get_lobby(message.text)
    answer_text = 'Такой комнаты не существует'
    reply_markup = kb_menu
    if user_lobby is not None:
        if message.from_user.id in user_lobby.get_users_id():
            if message.from_user.id == user_lobby.get_admin_id():
                answer_text = 'Название: {0}. Роль: admin'.format(
                    user_lobby.get_name(),
                )
                reply_markup = ikb_admin_lobby_menu
            else:
                answer_text = 'Название: {0}. Роль: user '.format(
                    user_lobby.get_name(),
                )
                reply_markup = ikb_lobby_menu
        logger.info('{0} chose the lobby'.format(
            message.from_user.full_name,
        ))
    await state.finish()

    await message.answer(answer_text, reply_markup=reply_markup)
    message = await message.answer('fake', reply_markup=kb_menu)
    await message.delete()


@dispatcher.callback_query_handler(text='distribute')
async def distribute(call: CallbackQuery):
    last_character_lobby_name = -13
    lobby_name = call.message.text[10:last_character_lobby_name]
    logger.info('{0} started the distribution of players in the lobby {1}'.format(
        call.from_user.full_name,
        lobby_name,
    ))

    user_lobby = lobbies.get_lobby(lobby_name)
    if user_lobby is None:
        answer_text = 'Комната {0} удалена'.format(lobby_name)
        logger_text = '{0} is notified that lobby {1} has been deleted'.format(
            call.from_user.full_name,
            lobby_name,
        )
    elif user_lobby.is_lobby_open():
        user_lobby.close_lobby()
        user_lobby.shuffle()
        users_info = user_lobby.get_users_info()

        for index, user_info in enumerate(users_info):
            try:
                await dispatcher.bot.send_message(
                    chat_id=user_info.id,
                    text='Игра началась! \nВам выпал: {0}'.format(
                        users_info[index - 1].name,
                    ),
                )
                logger.info('Message was sent to {0} with the gifted'.format(
                    user_info.name,
                ))
            except Exception as ex:
                logger.error('{0} did not receive a message with the gifted. Ex: {1}'.format(
                    user_info.name,
                    ex,
                ))
        answer_text = 'Распределено'.format(lobby_name)
        logger_text = 'The distribution of players in lobby {0} is over'.format(
            lobby_name,
        )
    else:
        answer_text = 'Участники уже распределены'
        lg_text1 = '{0} received a response from the the distribute command in the lobby {1}'
        lg_text2 = 'that players are distributed'
        logger_text = ''.join([lg_text1 + lg_text2]).format(
            call.from_user.full_name,
            lobby_name,
        )

    await call.message.answer(text=answer_text, reply_markup=kb_menu)
    logger.info(logger_text)


@dispatcher.callback_query_handler(text='gifted')
async def gifted(call: CallbackQuery):
    last_character_lobby_name = -13
    lobby_name = call.message.text[10:last_character_lobby_name]
    logger.info('{0} called the gifted command in the lobby {1}'.format(
        call.from_user.full_name,
        lobby_name,
    ))
    user_lobby = lobbies.get_lobby(lobby_name)
    answer_text = ''

    if user_lobby is None:
        answer_text = 'Комната {0} удалена'.format(lobby_name)
        logger_text = '{0} is notified that lobby {1} has been deleted'.format(
            call.from_user.full_name,
            lobby_name,
        )
    elif user_lobby.is_lobby_open():
        answer_text = 'Участники не распределены'
        lg_text1 = '{0} received a response from the the gifted command in the lobby {1}'
        lg_text2 = 'that players are not distributed'
        logger_text = ''.join([lg_text1 + lg_text2]).format(
            call.from_user.full_name,
            lobby_name,
        )
    else:
        users_info = user_lobby.get_users_info()
        for index, user_info in enumerate(users_info):
            if user_info.id == call.from_user.id:
                answer_text = 'Вам выпал: {0}'.format(
                        users_info[index - 1].name,
                    )
                break
        logger_text = '{0} received a response from the the gifted command in the lobby {1}'.format(
            call.from_user.full_name,
            lobby_name,
        )

    await call.message.answer(
        text=answer_text,
        reply_markup=kb_menu,
    )
    logger.info(logger_text)


@dispatcher.callback_query_handler(text='players')
async def players(call: CallbackQuery):
    last_character_lobby_name = -13
    lobby_name = call.message.text[10:last_character_lobby_name]
    logger.info('{0} called the players command in the lobby {1}'.format(
        call.from_user.full_name,
        lobby_name,
    ))
    user_lobby = lobbies.get_lobby(lobby_name)
    if user_lobby is None:
        answer_text = 'Комната {0} удалена'.format(lobby_name)
        logger_text = '{0} is notified that lobby {1} has been deleted'.format(
            call.from_user.full_name,
            lobby_name,
        )
    else:
        answer_text = 'Участники:\n'
        answer_text += ', '.join(user_info.name for user_info in sorted(user_lobby.get_users_info()))
        logger_text = '{0} received a response from the players command in the lobby {1}'.format(
            call.from_user.full_name,
            lobby_name,
        )
    await call.message.answer(
        text=answer_text,
        reply_markup=kb_menu,
    )
    logger.info(logger_text)


@dispatcher.callback_query_handler(text='delete')
async def delete(call: CallbackQuery):
    last_character_lobby_name = -13
    lobby_name = call.message.text[10:last_character_lobby_name]
    logger.info('{0} called the delete command in the lobby {1}'.format(
        call.from_user.full_name,
        lobby_name,
    ))
    user_lobby = lobbies.get_lobby(lobby_name)
    if user_lobby is None:
        await call.message.answer(
            text='Комната {0} удалена'.format(lobby_name),
            reply_markup=kb_menu,
        )
        logger_text = '{0} is notified that lobby {1} has been deleted'.format(
            call.from_user.full_name,
            lobby_name,
        )
    else:
        users_info = user_lobby.get_users_info()
        for user_info in users_info:
            try:
                await dispatcher.bot.send_message(
                    chat_id=user_info.id,
                    text='Комната {0} удалена!'.format(
                        lobby_name
                    ),
                )
                logger.info('{0} is notified of the removal of the lobby {1}'.format(
                    user_info.name,
                    lobby_name,
                ))
            except Exception as ex:
                logger.error('{0} did not notified of the removal of the lobby {1}. Ex: {2}'.format(
                    user_info.name,
                    lobby_name,
                    ex,
                ))
        lobbies.remove_lobby(user_lobby)
        logger_text = 'Lobby {0} removed by {1}'.format(
            lobby_name,
            call.from_user.full_name,
        )
    logger.info(logger_text)


@dispatcher.callback_query_handler(text='leave')
async def leave(call: CallbackQuery):
    last_character_lobby_name = -13
    lobby_name = call.message.text[10:last_character_lobby_name]
    logger.info('{0} called the leave command in the lobby {1}'.format(
        call.from_user.full_name,
        lobby_name,
    ))
    user_lobby = lobbies.get_lobby(lobby_name)
    if user_lobby is None:
        answer_text = 'Комната {0} удалена'.format(lobby_name)
        logger_text = '{0} is notified that lobby {1} has been deleted'.format(
            call.from_user.full_name,
            lobby_name,
        )
    elif user_lobby.is_open() is False:
        answer_text = 'Вы не можете покинуть данную комнату. Игра уже началась'
        logger_text = '{0} is notified that he cannot leave the lobby {1} because the game has already started'.format(
            call.from_user.full_name,
            lobby_name,
        )
    elif call.from_user.id not in user_lobby.get_users_id():
        answer_text = 'Вы уже покинули комнату {0}'.format(lobby_name)
        logger_text = '{0} is notified that he has already left the lobby {1}'.format(
            call.from_user.full_name,
            lobby_name,
        )
    else:
        answer_text = 'Вы покинули комнату {0}'.format(lobby_name)
        logger_text = '{0} receives a notification that he has left the lobby {1}'.format(
            call.from_user.full_name,
            lobby_name,
        )
        user_lobby.remove_user(call.from_user.id, call.from_user.full_name)
    await call.message.answer(
        text=answer_text,
        reply_markup=kb_menu,
    )
    logger.info(logger_text)
