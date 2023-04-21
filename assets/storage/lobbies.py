from loguru import logger

from assets.storage.lobby import Lobby


def is_name_corrected(name: str) -> bool:
    if len(name) == 0:
        return False
    elif name[0] == '/':
        return False
    return True


class Lobbies:
    __instance = None
    lobbies: dict[str: Lobby] = dict()

    def __init__(self):
        if not Lobbies.__instance:
            logger.info(' __init__ method of class Lobbies called..')
        else:
            logger.info('Instance of class Lobbies already created: {0}'.format(
                self.get_instance(),
            ))

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Lobbies()
        return cls.__instance

    def is_name_occupied(self, name: str) -> bool:
        return name in self.lobbies

    def add_lobby(self, lobby: Lobby):
        self.lobbies[lobby.name] = lobby

    def remove_lobby(self, lobby: Lobby):
        del self.lobbies[lobby.name]

    def get_lobby(self, name: str) -> Lobby | None:
        return self.lobbies.get(name)

    def get_user_lobbies(self, user_id: str) -> list:
        user_lobbies = []
        lobbies = self.lobbies.values()
        for lobby in lobbies:
            if user_id == lobby.get_admin_id():
                user_lobbies.append([lobby.name, 'admin'])
            elif user_id in lobby.get_users_id():
                user_lobbies.append([lobby.name, 'user'])
        return user_lobbies
