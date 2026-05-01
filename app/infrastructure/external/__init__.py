"""Módulo de integração com sistemas externos.

Contém interfaces abstratas e implementações para comunicação com APIs externas
como TMDB, sem acoplar a camada de domínio a detalhes técnicos.
"""

from app.infrastructure.external.movie_data_source_interface import IMovieDataSource
from app.infrastructure.external.tmdb_data_source import TMDBDataSource

__all__ = [
    "IMovieDataSource",
    "TMDBDataSource",
]
