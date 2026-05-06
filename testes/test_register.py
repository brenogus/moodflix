from app.application.use_cases.register_user import RegisterUser
from app.repositories.memory_user_repository import MemoryUserRepository

# 1. Instanciamos o repositório (nosso "banco" fake)
repo = MemoryUserRepository()

# 2. Instanciamos o caso de uso passando o repositório
use_case = RegisterUser(repo)

# 3. Tentamos cadastrar um usuário
try:
    user_in_db = use_case.execute({"username": "gabriel", "password": "123"})
    print(f"Sucesso: {user_in_db}")
    
    # 4. Tentamos cadastrar o MESMO usuário (deve dar erro)
    use_case.execute({"username": "gabriel", "password": "abc"})
except ValueError as e:
    print(f"Erro esperado: {e}")