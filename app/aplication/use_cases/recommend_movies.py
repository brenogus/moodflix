"""Use Case de Recomendação de Filmes.

Use cases encapsulam as regras de negócio e orquestram a interação
entre entidades de domínio e repositórios.
Faz parte da camada de Application (Clean Architecture).
"""

import logging
from typing import List, Optional
from app.domain.repositories.movie_repository_interface import IMovieRepository
from app.domain.services.mood_recommendation_service import get_mood_recommendation_service
from app.domain.entities.movie import Movie

logger = logging.getLogger(__name__)


def recommend_movies(
    repository: IMovieRepository,
    genre: Optional[str] = None,
    mood: Optional[str] = None
) -> List[Movie]:
    """Use case para recomendação de filmes.
    
    Orquestra a lógica de negócio: busca filmes por gênero ou mood
    e retorna as recomendações. Este é o ponto de entrada para a regra de negócio.
    
    Princípios aplicados:
    - **Dependency Injection**: Depende APENAS de abstrações (IMovieRepository)
    - **Fail-Safe**: Retorna lista vazia em caso de erro
    - **Separation of Concerns**: Use case não conhece detalhes de implementação
    - **Single Responsibility**: Responsável apenas pela orquestração da recomendação
    
    Args:
        repository: Implementação do repositório de filmes (injeção de dependência).
                   Não pode ser None.
        genre: Gênero para filtrar filmes (ex: 'acao', 'comedia', 'drama').
               Opcional.
        mood: Estado emocional do usuário para recomendação personalizada
              (ex: 'feliz', 'triste', 'pensativo', 'romantico').
              Opcional.
        
    Returns:
        Lista de entidades Movie do domínio, ordenadas por rating.
        Retorna lista vazia se:
        - Nenhum parâmetro de busca foi fornecido
        - Gênero/mood não foram encontrados
        - Ocorreu erro durante processamento
        
    Raises:
        Nenhuma exceção é lançada. Método é fail-safe.
        
    Example:
        >>> from app.repositories.movie_repository import MovieRepositoryFactory
        >>> repo = MovieRepositoryFactory.get_repository()
        >>> filmes = recommend_movies(repository=repo, genre='acao')
        >>> print(len(filmes))
        10
        
    Fluxo da Execução:
        1. Valida se algum parâmetro de busca foi fornecido
        2. Se 'genre': chama repository.get_by_genre()
        3. Se 'mood': chama MoodRecommendationService
        4. Retorna lista de filmes ou lista vazia em erro
    """
    try:
        if not repository:
            logger.error("Repositório não pode ser None")
            return []
        
        if genre:
            logger.info(f"Executando recomendação por gênero: '{genre}'")
            movies = repository.get_by_genre(genre, limit=10)
            logger.debug(f"Repository retornou {len(movies)} filme(s) para gênero '{genre}'")
            return movies
            
        elif mood:
            logger.info(f"Executando recomendação por mood: '{mood}'")
            mood_service = get_mood_recommendation_service()
            movies = mood_service.get_recommendations(mood=mood)
            logger.debug(f"MoodService retornou {len(movies)} filme(s) para mood '{mood}'")
            return movies
            
        else:
            logger.warning(
                "Nenhum parâmetro de busca fornecido. "
                "Use 'genre' ou 'mood' para obter recomendações."
            )
            return []

    except Exception as e:
        logger.error(
            f"Erro crítico no use case de recomendação (genre={genre}, mood={mood}): {e}",
            exc_info=True
        )
        return []