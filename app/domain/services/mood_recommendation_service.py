"""Serviço de Domínio de Recomendação por Mood.

Implementa a lógica de recomendação baseada no estado emocional do usuário.
Faz parte da camada de Domain (Clean Architecture).
"""

import logging
from typing import List, Dict, Optional
from app.domain.entities.movie import Movie
from app.domain.services.domain_service_interface import IDomainService

logger = logging.getLogger(__name__)


class MoodRecommendationService(IDomainService):
    """Serviço de domínio para recomendações por mood.
    
    Implementa a lógica de negócio de recomendação de filmes
    baseado no estado emocional (mood) do usuário.
    
    Attributes:
        mood_map: Dicionário mapeando moods para listas de filmes recomendados
    
    Example:
        >>> service = MoodRecommendationService()
        >>> filmes = service.get_recommendations(mood="feliz")
        >>> print(len(filmes))
        2
    """
    
    # Mapa de moods para recomendações de filmes
    MOOD_MAP: Dict[str, List[Movie]] = {
        "triste": [
            Movie(
                title="Á Procura da Felicidade",
                genre="drama",
                rating=8.0,
                release_year=2006
            ),
            Movie(
                title="Soul",
                genre="animacao",
                rating=8.1,
                release_year=2020
            )
        ],
        "feliz": [
            Movie(
                title="Se Beber Não Case",
                genre="comedia",
                rating=8.9,
                release_year=2009
            ),
            Movie(
                title="As Branquelas",
                genre="comedia",
                rating=7.8,
                release_year=2004
            )
        ],
        "pensativo": [
            Movie(
                title="Interestelar",
                genre="ficção científica",
                rating=8.6,
                release_year=2014
            ),
            Movie(
                title="A Origem",
                genre="ficção científica",
                rating=9.0,
                release_year=2010
            )
        ],
        "romantico": [
            Movie(
                title="Diário de uma Paixão",
                genre="romance",
                rating=7.6,
                release_year=2004
            )
        ]
    }

    def __init__(self):
        """Inicializa o serviço de recomendação por mood."""
        self.mood_map = self.MOOD_MAP.copy()
        logger.debug("MoodRecommendationService inicializado")

    def get_recommendations(self, mood: Optional[str] = None, **kwargs) -> List[Movie]:
        """Retorna filmes recomendados para um mood específico.
        
        Args:
            mood: Estado emocional do usuário.
                  Moods suportados: 'triste', 'feliz', 'pensativo', 'romantico'
            **kwargs: Argumentos adicionais (ignorados)
            
        Returns:
            Lista de filmes recomendados para o mood.
            Retorna lista vazia se mood não é reconhecido.
            
        Raises:
            N/A - Método fail-safe, retorna lista vazia em caso de erro
            
        Example:
            >>> service = MoodRecommendationService()
            >>> filmes = service.get_recommendations(mood="feliz")
            >>> for filme in filmes:
            ...     print(f"{filme.title} - {filme.rating}")
            Se Beber Não Case - 8.9
            As Branquelas - 7.8
        """
        if not mood:
            logger.warning("Mood não fornecido para recomendação")
            return []

        mood_lower = mood.lower().strip()
        recommendations = self.mood_map.get(mood_lower, [])
        
        if not recommendations:
            logger.warning(
                f"Mood desconhecido: '{mood}'. "
                f"Moods suportados: {', '.join(self.mood_map.keys())}"
            )
        else:
            logger.info(
                f"Recomendações geradas para mood: '{mood}' - "
                f"{len(recommendations)} filme(s) retornado(s)"
            )
        
        return recommendations
    
    def add_mood_recommendation(self, mood: str, movie: Movie) -> None:
        """Adiciona uma recomendação para um mood específico.
        
        Args:
            mood: Nome do mood
            movie: Entidade Movie a adicionar
            
        Raises:
            ValueError: Se mood ou movie são None/inválidos
        """
        if not mood or not isinstance(mood, str):
            raise ValueError("Mood deve ser uma string não-vazia")
        if not isinstance(movie, Movie):
            raise ValueError("Movie deve ser uma instância de Movie")
        
        mood_lower = mood.lower().strip()
        if mood_lower not in self.mood_map:
            self.mood_map[mood_lower] = []
        
        self.mood_map[mood_lower].append(movie)
        logger.info(f"Recomendação adicionada: '{movie.title}' para mood '{mood}'")


def get_mood_recommendation_service() -> MoodRecommendationService:
    """Factory function para obter instância do serviço de mood.
    
    Returns:
        Instância de MoodRecommendationService
        
    Note:
        Cada chamada retorna uma nova instância.
        Para Singleton, use um container de DI.
    """
    return MoodRecommendationService()