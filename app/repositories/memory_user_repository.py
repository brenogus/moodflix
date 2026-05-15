from typing import Optional, List
from app.domain.entities.user import User
from app.domain.repositories.user_repository_interface import IUserRepository

class MemoryUserRepository(IUserRepository):
    def __init__(self):
        # Simulamos o banco de dados com uma lista em memória
        self._users: List[User] = []

    def get_by_id(self, user_id: str) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users:
            if user.username == username:
                return user
        return None

    def exists(self, username: str) -> bool:
        return any(user.username == username for user in self._users)

    def save(self, user: User) -> None:
        # Se o usuário já existe (mesmo ID), atualizamos. Se não, adicionamos.
        existing_user = self.get_by_id(user.id)
        if existing_user:
            index = self._users.index(existing_user)
            self._users[index] = user
            return 
        else:
            self._users.append(user)
            return 