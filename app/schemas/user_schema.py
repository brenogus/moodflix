from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    message: str
    token: Optional[str] = None

class UserLogout(BaseModel):
    token: str

class UserLogoutResponse(BaseModel):
    message: str