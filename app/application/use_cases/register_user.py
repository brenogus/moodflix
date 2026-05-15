import uuid
from typing import Dict, Any
from app.domain.entities.user import User
from app.domain.repositories.user_repository_interface import IUserRepository

class RegisterUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a lógica de negócio para cadastrar um novo usuário.
        """
        username = user_data.get("username")
        password = user_data.get("password")

        # 1. Regra de Negócio: O username deve ser único
        if self.user_repository.exists(username):
            raise ValueError("Este nome de usuário já está em uso.")

        # 2. Segurança: Hash da senha 
        # (Aqui você chamaria uma função de hash. Nunca salve em texto puro!)
        password_hash = f"hashed_{password}" 

        # 3. Criação da Entidade
        # Usamos uuid para garantir um ID único e aleatório
        new_user = User(
            id=str(uuid.uuid4()),
            username=username,
            password_hash=password_hash,
            moodmap_list=[],
            default_moodmap= None
        )

        # 4. Persistência
        self.user_repository.save(new_user)

        # 5. Retorno (Geralmente retornamos os dados públicos do usuário)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "message": "Usuário cadastrado com sucesso!",
            
        }