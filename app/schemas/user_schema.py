from pydantic import BaseModel, Field
from typing import Optional,Dict

class UserResponse(BaseModel):
    id_user : str = Field(..., description="Chave primaria para identificar o usuário", min_length=1)
    user_name : str =Field(..., description="User name do usuário, seu nick name", min_length=1)
    mood_map : Dict[str : str]

    class Config:
        """Configuracao do Pydantic BaseModel."""
        json_schema_extra = {
            "example": {
                "id_user": "123456",
                "use_name": "SenhoraSmurfete",
                "mood_map": {
                                "romantico": "romance",
                                "feliz":"comedia"
                            }
            }
        }


class UserLoginRequest(BaseModel):
    user_name: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    mood_map: Dict[str, str]        