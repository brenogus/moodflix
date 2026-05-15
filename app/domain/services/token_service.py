from datetime import datetime, timedelta
from app.domain.entities.user import User
import jwt
from app.config import settings
from app.domain.repositories.blacklist_repository_interface import IBlacklistRepository
import logging


logger = logging.getLogger(__name__)

def create_token(user : User= None): # gera um novo JWT
    if user:
        payload = {
            "sub":user.id,
            "exp": (datetime.now() + timedelta(hours=24)).timestamp(),
            "iat": datetime.now().timestamp()
        }
        token = jwt.encode(payload,settings.SECRET_KEY,"HS256")
        return token
    else:
            return False


def verify_token(token : str= None): # verifica se o token é válido e retorna o payload
    if token:
         payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
         return payload
    else: return False

def is_blacklisted(token : str = None, blacklist_repository : IBlacklistRepository = None): # verifica se o token foi invalidado
    if token and blacklist_repository:
        return blacklist_repository.exists(token)
    else:
         return False
         

def blacklist_token(token, blacklist_repository: IBlacklistRepository): # adiciona o token na blacklist
    if token and blacklist_repository:
         logger.info("Chamando add_token do repositorio blacklist")
         return blacklist_repository.add_token(token)
    else:
         return False