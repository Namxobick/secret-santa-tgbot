import aiogram
from loguru import logger

from assets.secret_santa_loader import dispatcher
from assets.states.create_lobby_states import CreateLobbyStates
from assets.storage.lobbies import Lobbies, is_name_corrected
from assets.storage.lobby import Lobby
from assets.utils.misc import rate_limit

lobbies = Lobbies.get_instance()


@rate_limit(limit=2, key='/create_lobby')
@dispatcher.message_handler(aiogram.dispatcher.filters.Command('create_lobby'))
async def command_create_lobby(message: aiogram.types.Message):
    logger.info('{0} called the create_lobby command'.format(
        message.from_user.full_name,
    ))
    await message.answer('Введите название комнаты')
    await CreateLobbyStates.lobby_name.set()


@dispatcher.message_handler(state=CreateLobbyStates.lobby_name)
async def state_lobby_name(
    message: aiogram.types.Message,
    state: aiogram.dispatcher.FSMContext,
):
    answer = message.text
    is_name_occupied = lobbies.is_name_occupied(name=answer)
    if is_name_occupied or not is_name_corrected(name=answer):
        await state.finish()
        if lobbies.is_name_occupied(name=answer):
            answer_text = 'Данное название занято. Введите другое'
        else:
            answer_text = 'Данное название некорректно. Введите другое'
        await message.answer(answer_text)
        await CreateLobbyStates.lobby_name.set()
    else:
        await message.answer('Введите пароль')
        await state.update_data(lobby_name=answer)
        await CreateLobbyStates.lobby_password.set()


@dispatcher.message_handler(state=CreateLobbyStates.lobby_password)
async def state_lobby_password(
    message: aiogram.types.Message,
    state: aiogram.dispatcher.FSMContext,
):
    answer = message.text
    await state.update_data(lobby_password=answer)

    lobby_data = await state.get_data()
    lobby_name = lobby_data.get('lobby_name')
    lobby_password = lobby_data.get('lobby_password')
    lobby = Lobby(
        lobby_name,
        lobby_password,
        message.from_user.id,
        message.from_user.full_name,
    )
    lobbies.add_lobby(lobby)
    await message.answer('Комната успешно создана')
    await state.finish()

    logger.info('{0} received a response from the create_lobby command'.format(
        message.from_user.full_name,
    ))
