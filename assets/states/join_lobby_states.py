from aiogram.dispatcher.filters.state import State, StatesGroup


class JoinLobbyStates(StatesGroup):
    lobby_name = State()
    lobby_password = State()
