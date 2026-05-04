"""Fonte de Dados TMDB - Implementacao de IMovieDataSource.

Implementa a abstracao IMovieDataSource usando a API TMDB.
Faz parte da camada de Infrastructure (Clean Architecture).
"""

import logging
from typing import List, Dict, Any
from app.infrastructure.external.tmdb_client import fetch_movies_by_genre
from app.infrastructure.external.movie_data_source_interface import IMovieDataSource

logger = logging.getLogger(__name__)


class TMDBDataSource(IMovieDataSource):
    """Implementacao de fonte de dados usando a API TMDB.
    
    Implementa a interface IMovieDataSource, centralizando toda a logica
    de comunicacao com a API TMDB nesta classe.
    
    Responsabilidades:
    - Implementar o contrato de IMovieDataSource
    - Adaptar chamadas da API TMDB para o formato esperado
    - Tratar erros de comunicacao de forma robusta
    - Fazer cache de dados se necessario (futuro)
    
    Caracteristicas:
    - **Adapter Pattern**: Adapta API TMDB ao contrato IMovieDataSource
    - **Fail-Safe**: Retorna lista vazia em caso de erro
    - **Logging**: Registra todas as chamadas e erros
    
    Example:
        >>> data_source = TMDBDataSource()
        >>> filmes = data_source.fetch_by_genre(28)  # Acao
        >>> print(len(filmes))
        20
    """

     # Mapeamento de gêneros em português para IDs da TMDB
    GENRE_MAP = {
        "acao": 28,
        "comedia": 35,
        "ficcao": 878,
        "drama": 18,
        "terror": 27,
        "romance": 10749,
        "animacao": 16
    }

    def __init__(self):
        """Inicializa a fonte de dados TMDB."""
        logger.debug("TMDBDataSource inicializado")

    def fetch_by_genre(self, genre_id: int) -> List[Dict[str, Any]]:
        """Busca filmes da API TMDB por genero.
        
        Chama a API TMDB atraves de fetch_movies_by_genre() e retorna
        os dados brutos.
        
        Args:
            genre_id: ID numerico do genero no TMDB
                     Exemplos: 28 (Acao), 35 (Comedia), 18 (Drama)
            
        Returns:
            Lista de dicionarios com dados dos filmes da TMDB.
            Cada dicionario contem: title, vote_average, overview, release_date, etc.
            Retorna lista vazia se ocorrer erro.
            
        Raises:
            Nenhuma excecao e lancada (fail-safe).
            
        Example:
            >>> data_source = TMDBDataSource()
            >>> filmes = data_source.fetch_by_genre(28)  # Filmes de Acao
            >>> for filme in filmes[:3]:
            ...     print(f"{filme['title']} - {filme['vote_average']}")
        """
        try:
            if not isinstance(genre_id, int) or genre_id <= 0:
                logger.warning(f"Genre ID invalido: {genre_id}")
                return []
            
            logger.debug(f"Buscando filmes do TMDB para genre_id: {genre_id}")
            movies_data = fetch_movies_by_genre(genre_id)
            logger.info(f"Retornando {len(movies_data)} filmes do TMDB para genre_id {genre_id}")
            return movies_data
        except Exception as e:
            logger.error(
                f"Erro ao buscar dados do TMDB para genre_id {genre_id}: {e}",
                exc_info=True
            )
            return []
