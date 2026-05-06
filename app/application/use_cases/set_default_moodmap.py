from typing import Dict, Any
from app.domain.repositories.user_repository_interface import IUserRepository

class SetDefaultMoodMap:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str, moodmap_id: str) -> Dict[str, Any]:
        """
        Define um MoodMap específico como o padrão para o usuário.
        """
        # 1. Busca o usuário
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        # 2. Delega a lógica para a entidade
        # A entidade User vai validar se esse moodmap_id realmente existe na lista
        user.set_default_moodmap(moodmap_id)

        # 3. Salva a alteração no repositório
        self.user_repository.save(user)

        return {
            "message": "MoodMap padrão atualizado!",
            "default_moodmap": user.default_moodmap
        }