from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateLobbyStates(StatesGroup):
    lobby_name = State()
    lobby_password = State()
