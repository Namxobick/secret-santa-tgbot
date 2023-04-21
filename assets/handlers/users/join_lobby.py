import aiogram
from loguru import logger

from assets.secret_santa_loader import dispatcher
from assets.states.join_lobby_states import JoinLobbyStates
from assets.storage.lobbies import Lobbies
from assets.utils.misc import rate_limit

lobbies = Lobbies.get_instance()


@rate_limit(limit=2, key='/join_lobby')
@dispatcher.message_handler(aiogram.dispatcher.filters.Command('join_lobby'))
async def command_create_lobby(message: aiogram.types.Message):
    logger.info('{0} called the join_lobby command'.format(
        message.from_user.full_name,
    ))
    await message.answer('Введите название комнаты')
    await JoinLobbyStates.lobby_name.set()


@dispatcher.message_handler(state=JoinLobbyStates.lobby_name)
async def state_lobby_name(
    message: aiogram.types.Message,
    state: aiogram.dispatcher.FSMContext,
):
    answer = message.text

    if lobbies.is_name_occupied(name=answer):
        await state.update_data(lobby_name=answer)
        await message.answer('Введите пароль')
        await JoinLobbyStates.lobby_password.set()
    else:
        await state.finish()
        await message.answer('Такой комнаты не существует')


@dispatcher.message_handler(state=JoinLobbyStates.lobby_password)
async def state_lobby_password(
    message: aiogram.types.Message,
    state: aiogram.dispatcher.FSMContext,
):
    answer = message.text
    lobby_data = await state.get_data()
    lobby = lobbies.get_lobby(lobby_data.get('lobby_name'))

    if lobby.get_password() != answer:
        await message.answer('Не верный пароль')
    elif message.from_user.id in lobby.get_users_id():
        await message.answer('Вы уже состоите в данной комнате')
    elif lobby.is_open() is False:
        await message.answer('Комната закрыта')
    else:
        lobby.add_user(message.from_user.id, message.from_user.full_name)
        await message.answer('Вы присоединились к комнате')
    await state.finish()

    logger.info('{0} received a response from the join_lobby command'.format(
        message.from_user.full_name,
    ))
