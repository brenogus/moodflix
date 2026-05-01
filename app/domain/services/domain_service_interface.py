"""Interface de Serviço de Domínio.

Define o contrato para serviços que encapsulam lógica de negócio.
Faz parte da camada de Domain (Clean Architecture).
"""

from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.movie import Movie


class IDomainService(ABC):
    """Interface para serviços de domínio.
    
    Serviços de domínio encapsulam lógica complexa de negócio
    que não pertence a uma entidade ou use case específico.
    
    Exemplo: Recomendações baseadas em mood, cálculos complexos,
    algoritmos de recomendação, etc.
    """
    
    @abstractmethod
    def get_recommendations(self, **kwargs) -> List[Movie]:
        """Retorna recomendações baseado em critérios.
        
        Returns:
            Lista de filmes recomendados
        """
        pass
