from app.repositories.memory_user_repository import MemoryUserRepository
from app.application.use_cases.register_user import RegisterUser
from app.application.use_cases.login_user import LoginUser
from app.application.use_cases.add_moodmap import AddMoodMap
from app.application.use_cases.set_default_moodmap import SetDefaultMoodMap

def run_test():
    repo = MemoryUserRepository()
    
    # Instanciando todos os serviços
    register_service = RegisterUser(repo)
    login_service = LoginUser(repo)
    add_mood_service = AddMoodMap(repo)
    set_default_service = SetDefaultMoodMap(repo)

    print("--- Iniciando Teste de Fluxo Completo ---")

    # 1. Cadastro e Login
    user_data = {"username": "gabriel_dev", "password": "123"}
    new_user = register_service.execute(user_data)
    auth = login_service.execute(user_data)
    user_id = auth['id']

    # 2. Adicionando um MoodMap
    # Vamos incluir um ID manual para facilitar a busca no set_default
    meu_mood = {"moodmap_id": "map_001", "name": "Foco Total", "genre": "Lofi"}
    res_add = add_mood_service.execute(user_id, meu_mood)
    print(f"[MOOD] {res_add['message']} Total: {res_add['total_maps']}")

    # 3. Definindo como padrão
    res_default = set_default_service.execute(user_id, "map_001")
    print(f"[DEFAULT] {res_default['message']}")
    print(f"DEBUG: Mood atual é {res_default['default_moodmap']['name']}")

    # 4. Teste de Limite (Tentando adicionar mais de 5)
    print("\n--- Testando Limite de 5 MoodMaps ---")
    try:
        for i in range(10):
            add_mood_service.execute(user_id, {"moodmap_id": f"id_{i}", "name": "Teste"})
    except ValueError as e:
        print(f"Sucesso no teste de erro: {e}")

if __name__ == "__main__":
    run_test()