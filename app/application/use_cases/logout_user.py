from app.domain.services.token_service import blacklist_token
from app.domain.repositories.blacklist_repository_interface   import IBlacklistRepository
import logging


logger = logging.getLogger(__name__)

class LogoutUser:
    def __init__(self,blacklist_repository:IBlacklistRepository):
        self.blacklist_repository = blacklist_repository

    def execute(self,token: str):
        """Executa lógica de logout""" 
        try:
            if not token or not self.blacklist_repository:
                logger.error("Token ou blacklist não pode ser None.")
            else:
                logger.info("Entrada no fluxo de token")
                if blacklist_token(token,self.blacklist_repository):
                    return {"message":"Token adicionado na blacklist com sucesso."}
                else:
                    return {"message": "Falha ao adicionar token na blacklist"}
            
        except Exception as e:
            logger.error(
                f"Erro crítico no use case de logout : {e}",
                exc_info=True
            )
            return f"Erro de exceção {e}"   

    