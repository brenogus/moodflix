"""Entidade de domínio: Filme.

Representa um filme no sistema MoodFlix.
Faz parte da camada de Domain (Clean Architecture).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    """Entidade que representa um filme no domínio MoodFlix.
    
    Esta é uma entidade de domínio (Domain Entity) que encapsula
    as propriedades e comportamentos essenciais de um filme.
    Não tem dependências externas e representa um conceito puro do negócio.
    
    Attributes:
        title (str): Título do filme
        genre (str): Gênero do filme (ex: 'acao', 'comedia', 'drama')
        rating (float): Classificação do filme (0.0 a 10.0)
        description (Optional[str]): Descrição ou sinopse do filme
        release_year (Optional[int]): Ano de lançamento
    
    Example:
        >>> movie = Movie(
        ...     title="Interestelar",
        ...     genre="ficção científica",
        ...     rating=8.6,
        ...     release_year=2014
        ... )
        >>> print(movie.title)
        Interestelar
    """
    
    title: str
    genre: str
    rating: float
    description: Optional[str] = None
    release_year: Optional[int] = None
    
    def __post_init__(self):
        """Valida os atributos após inicialização.
        
        Raises:
            ValueError: Se rating não está entre 0.0 e 10.0
            ValueError: Se title ou genre estão vazios
        """
        if not self.title or not self.title.strip():
            raise ValueError("Título do filme não pode estar vazio")
        
        if not self.genre or not self.genre.strip():
            raise ValueError("Gênero do filme não pode estar vazio")
        
        if not (0.0 <= self.rating <= 10.0):
            raise ValueError(f"Rating deve estar entre 0.0 e 10.0, recebido: {self.rating}")
    
    def is_highly_rated(self, threshold: float = 7.0) -> bool:
        """Verifica se o filme tem alta classificação.
        
        Args:
            threshold: Valor mínimo de classificação (padrão: 7.0)
            
        Returns:
            True se o rating é >= threshold, False caso contrário
        """
        return self.rating >= threshold
