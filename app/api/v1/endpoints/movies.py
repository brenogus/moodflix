"""Endpoints da API v1 para Filmes.

Camada de Presentation que expoe os casos de uso como endpoints HTTP.
Faz parte da camada de Presentation/API (Clean Architecture).
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Query
from app.application.use_cases.recommend_movies import recommend_movies
from app.repositories.movie_repository import movie_repository
from app.schemas.movie_schema import MovieResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/movies", response_model=List[MovieResponse])
def list_movies(limit: int = Query(20, ge=1, le=100)):
    """Lista todos os filmes disponiveis.
    
    **Endpoint**: GET /api/v1/movies
    
    **Query Parameters**:
        - limit: Quantidade maxima de filmes (1-100, padrao: 20)
    
    **Responses**:
        - 200: Lista de filmes retornada com sucesso
    
    Args:
        limit: Numero maximo de filmes a retornar
        
    Returns:
        Lista de objetos MovieResponse com dados dos filmes
    
    Example:
        >>> GET /api/v1/movies?limit=10
        [
            {
                "title": "Interestelar",
                "genre": "ficcao",
                "rating": 8.6,
                "release_year": 2014
            }
        ]
    """
    try:
        logger.debug(f"GET /movies - limit: {limit}")
        
        # Implementacao futura: buscar filmes do repositorio
        logger.info("Endpoint /movies - retornando lista vazia (nao implementado)")
        return []
        
    except Exception as e:
        logger.error(f"Erro no endpoint /movies: {e}", exc_info=True)
        return []


@router.get("/recommend", response_model=List[MovieResponse])
def recommend(
    genre: Optional[str] = Query(
        None,
        description="Genero do filme (ex: acao, comedia, drama, ficcao, romance, animacao, terror)"
    ),
    mood: Optional[str] = Query(
        None,
        description="Estado emocional (ex: triste, feliz, pensativo, romantico)"
    )
):
    """Recomenda filmes baseado em genero ou mood.
    
    **Endpoint**: GET /api/v1/recommend
    
    **Query Parameters**:
        - genre: Genero para filtro (opcional)
                Valores: acao, comedia, drama, ficcao, romance, animacao, terror
        - mood: Estado emocional para recomendacao (opcional)
               Valores: triste, feliz, pensativo, romantico
    
    **Responses**:
        - 200: Lista de filmes recomendados
        - 400: Se nenhum parametro (genre ou mood) foi fornecido
    
    **Fluxo**:
        1. Recebe parametros de genre ou mood
        2. Chama use case recommend_movies() com o repositorio injetado
        3. Transforma entidades de dominio em DTOs (MovieResponse)
        4. Retorna lista de filmes recomendados
    
    Args:
        genre: Genero para filtro (opcional)
        mood: Estado emocional para recomendacao (opcional)
        
    Returns:
        Lista de objetos MovieResponse com recomendacoes
    
    Raises:
        Retorna lista vazia se nenhum parametro foi fornecido ou em erro
    
    Example:
        >>> GET /api/v1/recommend?genre=acao
        [
            {
                "title": "Homem de Ferro",
                "genre": "acao",
                "rating": 7.9,
                "release_year": 2008
            },
            {
                "title": "Capitao America",
                "genre": "acao",
                "rating": 8.4,
                "release_year": 2011
            }
        ]
    """
    try:
        logger.info(f"Recomendacao solicitada - genre: {genre}, mood: {mood}")
        
        # Valida que pelo menos um parametro foi fornecido
        if not genre and not mood:
            logger.warning("Nenhum parametro fornecido (genre ou mood)")
            return []
        
        # Use case orquestra a logica de negocio
        # Dependency Injection: repositorio injetado
        movies = recommend_movies(
            repository=movie_repository,
            genre=genre,
            mood=mood
        )
        
        # Adapter: Transforma entidades de dominio em DTOs para a API
        # Isso desacopla a camada de apresentacao do modelo de dominio
        response = [
            MovieResponse(
                title=movie.title,
                genre=movie.genre,
                rating=movie.rating,
                description=movie.description,
                release_year=movie.release_year
            )
            for movie in movies
        ]
        
        logger.info(f"Retornando {len(response)} filme(s) recomendado(s)")
        return response

    except Exception as e:
        logger.error(
            f"Erro no endpoint /recommend (genre={genre}, mood={mood}): {e}",
            exc_info=True
        )
        return []
