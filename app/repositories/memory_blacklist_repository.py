from typing import Dict
from app.domain.repositories.blacklist_repository_interface import IBlacklistRepository
from app.domain.services.token_service import verify_token
from datetime import datetime

class MemoryBlacklistRepository(IBlacklistRepository):
    def __init__(self):
        # Simulamos o banco de dados com uma lista em memória
        self._tokens: Dict[str] = {}

    def exists(self, token: str) -> bool:
         return token in self._tokens
        

    def add_token(self, token: str) -> bool:
       if not self.exists(token):
           payload = verify_token(token)
           self._tokens[token] = payload["exp"]
           return True
       else:
           return False

    

    def clear_expired_tokens(self) -> None:
        self._tokens = {
                            token: exp 
                            for token, exp in self._tokens.items() 
                            if exp > datetime.now().timestamp()
        }


