from typing import Dict, Any, Optional
from app.domain.repositories.user_repository_interface import IUserRepository
from app.domain.services.token_service import create_token

class LoginUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, login_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a lógica de autenticação.
        """
        username = login_data.get("username")
        password = login_data.get("password")

        # 1. Busca o usuário pelo username
        user = self.user_repository.get_by_username(username)

        # 2. Verifica se o usuário existe
        if not user:
            raise ValueError("Usuário ou senha incorretos.")

        # 3. Verificação de Senha
        # Em um cenário real, você usaria uma lib para comparar o hash:
        # if not password_hasher.verify(password, user.password_hash):
       
        expected_hash = f"hashed_{password}" # Simulando o hash que fizemos no cadastro
        if user.password_hash != expected_hash:
            raise ValueError("Usuário ou senha incorretos.")

        token = create_token(user)
        
        return {
            "id": user.id,
            "username": user.username,
            "message": "Login realizado com sucesso!",
            "token" : token
        }