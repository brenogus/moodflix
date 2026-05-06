from typing import Dict, Any
from app.domain.repositories.user_repository_interface import IUserRepository

class AddMoodMap:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str, mood_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Adiciona um novo mapeamento de humor para um usuário específico.
        """
        # 1. Busca o usuário no "banco"
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        # 2. Usa a lógica interna da Entidade User para adicionar
        # Lembre-se: a entidade User já valida o limite de 5 mapas!
        user.add_new_moodmap(mood_data)

        # 3. Persiste a alteração (o método save que explicamos antes faz o Update)
        self.user_repository.save(user)

        return {
            "message": "MoodMap adicionado com sucesso!",
            "total_maps": len(user.moodmap_list)
        }