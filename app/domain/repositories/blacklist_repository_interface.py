"""Interface do Repositório de blacklist.

Define o contrato para implementações de repositórios de blacklist.
Faz parte da camada de Domain (Clean Architecture).
"""

from abc import ABC, abstractmethod




class IBlacklistRepository(ABC):
    """Interface que define o contrato para operações com blacklist.
    
    Qualquer implementação de repositório deve seguir este contrato.
    Isso permite que Use Cases dependam de abstração, não de implementação.
    Segue o princípio de Inversão de Dependência (DIP).
    
    Esta interface pertence à camada de Domain, representando
    um conceito central do negócio.
    """
    @abstractmethod
    def add_token(self, token: str) -> bool:
        """Adiciona um token à blacklist."""
        pass

    @abstractmethod
    def exists(self, token: str) -> bool:
        """Verifica se o token está na blacklist."""
        pass

    @abstractmethod
    def clear_expired_tokens(self) -> None:
        """Limpa todos os token da blacklist caso ja tenha expirado"""
        pass

    