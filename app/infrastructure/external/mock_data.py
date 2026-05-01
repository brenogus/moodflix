"""Camada de dados mockados para teste e desenvolvimento.

Estes dados devem ser movidos para um banco de dados real em produção.
Esta camada faz parte da camada de infrastructure e pode ser
substituída por uma implementação real sem afetar as camadas superiores.
"""

from app.domain.entities.movie import Movie


class MockMovieData:
    """Gerencia dados mockados de filmes para testes."""

    GENRE_RECOMMENDATIONS = {
        "acao": [
            Movie("Mad Max", "acao", 8.2),
            Movie("John Wick", "acao", 7.9)
        ],
        "ficcao": [
            Movie("Interestelar", "ficcao", 8.6),
            Movie("Matrix", "ficcao", 8.7)
        ],
        "comedia": [
            Movie("Superbad", "comedia", 7.5),
            Movie("Se Beber Não Case", "comedia", 7.8)
        ]
    }

    MOOD_RECOMMENDATIONS = {
        "triste": [
            Movie("Á Procura da Felicidade", "drama", 8.0),
            Movie("Soul", "animacao", 8.1)
        ],
        "feliz": [
            Movie("Se Beber Não Case", "comedia", 8.9),
            Movie("As Branquelas", "comedia", 7.8)
        ],
        "pensativo": [
            Movie("Interestelar", "ficcao", 8.6),
            Movie("A Origem", "ficcao", 9.0)
        ],
        "romantico": [
            Movie("Diário de uma Paixão", "romance", 7.6)
        ]
    }

    @classmethod
    def get_by_genre(cls, genre: str):
        """Retorna filmes mockados por gênero."""
        return cls.GENRE_RECOMMENDATIONS.get(genre.lower(), [])

    @classmethod
    def get_by_mood(cls, mood: str):
        """Retorna filmes mockados por mood."""
        return cls.MOOD_RECOMMENDATIONS.get(mood.lower(), [])
