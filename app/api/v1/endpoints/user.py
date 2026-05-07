from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.application.use_cases.register_user import RegisterUser
from app.application.use_cases.login_user import LoginUser
from app.repositories.memory_user_repository import MemoryUserRepository

router = APIRouter()

# Instância única do repositório para persistência em memória
user_repo = MemoryUserRepository()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate):
    try:
        use_case = RegisterUser(user_repo)
        # O model_dump() do Pydantic v2 converte o objeto para dicionário
        return use_case.execute(user_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
def login(login_data: UserLogin):
    try:
        use_case = LoginUser(user_repo)
        return use_case.execute(login_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))