"""Interface do Repositório de Usuários.

Define o contrato para implementações de repositórios de usuários.
Faz parte da camada de Domain (Clean Architecture).
"""

from abc import ABC, abstractmethod
from typing import List, Optional,Dict
from app.domain.entities.user import User



class IUserRepository(ABC):
    """Interface que define o contrato para operações com users.
    
    Qualquer implementação de repositório deve seguir este contrato.
    Isso permite que Use Cases dependam de abstração, não de implementação.
    Segue o princípio de Inversão de Dependência (DIP).
    
    Esta interface pertence à camada de Domain, representando
    um conceito central do negócio.
    """
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca o usuário completo."""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca por username (essencial para login)."""
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        """Cria ou atualiza um usuário (incluindo seus moodmaps)."""
        pass

    @abstractmethod
    def exists(self, username: str) -> bool:
        """Verifica se o username já existe no cadastro."""
        pass