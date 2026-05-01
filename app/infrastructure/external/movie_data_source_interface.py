"""Interface para Fonte de Dados de Filmes.

Define o contrato para qualquer implementacao de fonte de dados.
Faz parte da camada de Infrastructure (Clean Architecture).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IMovieDataSource(ABC):
    """Interface para abstracao de fonte de dados de filmes.
    
    Define o contrato que qualquer implementacao de fonte de dados deve seguir.
    Permite que o repositorio nao dependa diretamente da implementacao
    (API TMDB, BD local, cache, etc).
    
    Principios:
    - **Inversao de Dependencia**: Repository depende desta interface
    - **Segregacao de Interface**: Apenas metodos necessarios
    - **Adapter Pattern**: Diferentes implementacoes da mesma interface
    
    Esta interface pertence a camada de Infrastructure, servindo como
    contrato entre Repository (Infrastructure) e Data Sources (externos).
    
    Implementacoes:
    - TMDBDataSource: Dados da API TMDB
    - MockDataSource: Dados mockados para testes
    - DatabaseDataSource: Dados de banco relacional (futuro)
    - CacheDataSource: Dados em cache (futuro)
    """

    @abstractmethod
    def fetch_by_genre(self, genre_id: int) -> List[Dict[str, Any]]:
        """Busca dados de filmes por genero.
        
        Contrato que todas as implementacoes devem seguir.
        
        Args:
            genre_id: ID numerico do genero (formato especifico de cada fonte)
                     Exemplos: 28 (TMDB Acao), 35 (TMDB Comedia)
            
        Returns:
            Lista de dicionarios com dados dos filmes.
            Cada dicionario deve conter minimamente:
            - "title": str - Titulo do filme
            - "vote_average": float - Classificacao (0.0 a 10.0)
            - "overview": str (opcional) - Sinopse
            - "release_date": str (opcional) - Data de lancamento
            
        Raises:
            Nenhuma excecao deve ser lancada. Implementacoes
            devem retornar lista vazia em caso de erro.
        
        Example:
            Implementacao TMDB:
            >>> ds = TMDBDataSource()
            >>> filmes = ds.fetch_by_genre(28)  # Acao
            >>> print(len(filmes))
            20
            >>> print(filmes[0]["title"])
            "Filme XYZ"
            
            Implementacao Mock:
            >>> ds = MockDataSource()
            >>> filmes = ds.fetch_by_genre(28)
            >>> print(len(filmes))
            2  # 2 filmes mockados
        """
        pass
