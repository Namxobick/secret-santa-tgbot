import random

from assets.storage.user import User


class Lobby:

    def __init__(self, name: str, password: str, admin_id: str, admin_name: str):
        self.name = name
        self.password = password
        self.admin_id = admin_id
        self.users_info = [User(admin_id, admin_name)]
        self.is_open = True

    def add_user(self, user_id: str, user_name: str):
        self.users_info.append(User(user_id, user_name))

    def get_name(self) -> str:
        return self.name

    def get_password(self) -> str:
        return self.password

    def get_admin_id(self) -> str:
        return self.admin_id

    def get_users_id(self) -> list[str]:
        users_id = []
        for user_info in self.users_info:
            users_id.append(user_info.id)
        return users_id

    def get_users_info(self) -> list[User]:
        return self.users_info

    def is_lobby_open(self) -> bool:
        return self.is_open

    def remove_user(self, user_id: str, user_name: str):
        self.users_info.remove(User(user_id, user_name))

    def close_lobby(self):
        self.is_open = False

    def shuffle(self):
        random.shuffle(self.users_info)
