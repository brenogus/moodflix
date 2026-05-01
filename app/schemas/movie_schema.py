"""Schemas (DTOs) para a API de Filmes.

Schemas definem os modelos de dados para requisicoes e respostas HTTP.
Usam Pydantic para validacao automatica.
Fazem parte da camada de Presentation (Clean Architecture).
"""

from pydantic import BaseModel, Field
from typing import Optional


class MovieResponse(BaseModel):
    """DTO (Data Transfer Object) para resposta de filme na API.
    
    Representa como um filme e retornado nos endpoints da API.
    Valida automaticamente os tipos de dados.
    
    Attributes:
        title: Titulo do filme
        genre: Genero do filme
        rating: Classificacao numerica (0.0 a 10.0)
        description: Descricao/sinopse (opcional)
        release_year: Ano de lancamento (opcional)
    
    Example:
        >>> filme = MovieResponse(
        ...     title="Interestelar",
        ...     genre="ficcao",
        ...     rating=8.6,
        ...     description="Um filme de ficção científica",
        ...     release_year=2014
        ... )
        >>> print(filme.title)
        Interestelar
    """
    
    title: str = Field(..., description="Titulo do filme", min_length=1)
    genre: str = Field(..., description="Genero do filme", min_length=1)
    rating: float = Field(..., description="Classificacao (0.0 a 10.0)", ge=0.0, le=10.0)
    description: Optional[str] = Field(None, description="Sinopse do filme")
    release_year: Optional[int] = Field(None, description="Ano de lancamento")

    class Config:
        """Configuracao do Pydantic BaseModel."""
        json_schema_extra = {
            "example": {
                "title": "Interestelar",
                "genre": "ficcao",
                "rating": 8.6,
                "description": "Um filme sobre viagens no espaco",
                "release_year": 2014
            }
        }