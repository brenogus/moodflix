import logging
import requests
from typing import List, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://api.themoviedb.org/3"


def fetch_movies_by_genre(genre_id: int) -> List[Dict[str, Any]]:
    """Busca filmes por gênero na API TMDB com tratamento de erros.
    
    Args:
        genre_id: ID do gênero na TMDB
        
    Returns:
        Lista de dicionários com dados dos filmes
        
    Raises:
        Retorna lista vazia em caso de erro (fail-safe)
    """
    try:
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "with_genres": genre_id,
            "language": "pt-BR"
        }

        logger.debug(f"Chamando TMDB API para gênero: {genre_id}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])
        
        logger.info(f"TMDB: {len(results)} filmes encontrados para gênero {genre_id}")
        return results

    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao chamar TMDB API para gênero {genre_id}")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP na TMDB API: {e.response.status_code} - {e}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na chamada TMDB API: {e}")
        return []
    except ValueError as e:
        logger.error(f"Erro ao fazer parse do JSON da TMDB: {e}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar filmes na TMDB: {e}")
        return []
