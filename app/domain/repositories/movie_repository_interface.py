"""Interface do Repositório de Filmes.

Define o contrato para implementações de repositórios de filmes.
Faz parte da camada de Domain (Clean Architecture).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.movie import Movie


class IMovieRepository(ABC):
    """Interface que define o contrato para operações com filmes.
    
    Qualquer implementação de repositório deve seguir este contrato.
    Isso permite que Use Cases dependam de abstração, não de implementação.
    Segue o princípio de Inversão de Dependência (DIP).
    
    Esta interface pertence à camada de Domain, representando
    um conceito central do negócio.
    """

    @abstractmethod
    def get_by_genre(self, genre: str, limit: int = 10) -> List[Movie]:
        """Busca filmes por gênero.
        
        Args:
            genre: Gênero do filme (ex: 'acao', 'comedia', 'drama')
            limit: Quantidade máxima de filmes a retornar (padrão: 10)
            
        Returns:
            Lista de filmes encontrados ordenados por rating descendente
            
        Raises:
            ValueError: Se o gênero é inválido ou vazio
        """
        pass
    
    @abstractmethod
    def get_all(self, limit: int = 20) -> List[Movie]:
        """Busca todos os filmes disponíveis.
        
        Args:
            limit: Quantidade máxima de filmes a retornar (padrão: 20)
            
        Returns:
            Lista de todos os filmes disponíveis
        """
        pass
    
    @abstractmethod
    def get_highly_rated(self, threshold: float = 7.0, limit: int = 10) -> List[Movie]:
        """Busca filmes com classificação alta.
        
        Args:
            threshold: Classificação mínima (padrão: 7.0)
            limit: Quantidade máxima de filmes a retornar (padrão: 10)
            
        Returns:
            Lista de filmes com rating >= threshold
        """
        pass
