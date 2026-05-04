"""Repositório de Filmes - Camada de Apresentação de Dados.

Implementação concreta de IMovieRepository que transforma dados externos
em entidades de domínio.
Faz parte da camada de Infrastructure (Clean Architecture).
"""

import logging
from typing import List, Optional
from app.domain.entities.movie import Movie
from app.domain.repositories.movie_repository_interface import IMovieRepository
from app.infrastructure.external.movie_data_source_interface import IMovieDataSource
from app.infrastructure.external.tmdb_data_source import TMDBDataSource

logger = logging.getLogger(__name__)


class MovieRepository(IMovieRepository):
    """Implementação concreta do repositório de filmes.
    
    Responsabilidades:
    - Transformar dados brutos de fontes externas em entidades de domínio
    - Implementar o contrato definido por IMovieRepository
    - Coordenar com a fonte de dados (IMovieDataSource)
    - Garantir integridade dos dados ao criar entidades
    
    Características:
    - **Inversão de Dependência**: Depende de IMovieDataSource, não de TMDB direto
    - **Adapter Pattern**: Adapta dados externos ao modelo de domínio
    - **Fail-Safe**: Retorna lista vazia em caso de erro
    - **Mapeamento de Gêneros**: Mapeia nomes de gêneros para IDs da TMDB
    
    Attributes:
        data_source: Implementação de IMovieDataSource para obter dados
    
    Example:
        >>> from app.infrastructure.external.tmdb_data_source import TMDBDataSource
        >>> data_source = TMDBDataSource()
        >>> repo = MovieRepository(data_source)
        >>> filmes = repo.get_by_genre('acao', limit=5)
        >>> print(len(filmes))
        5
    """
    
    

    def __init__(self, data_source: IMovieDataSource):
        """Inicializa o repositório com uma fonte de dados.
        
        Args:
            data_source: Implementação de IMovieDataSource que fornece dados brutos.
                        Pode ser TMDBDataSource, MockDataSource, DatabaseDataSource, etc.
            
        Raises:
            ValueError: Se data_source é None
            
        Example:
            >>> from app.infrastructure.external.tmdb_data_source import TMDBDataSource
            >>> data_source = TMDBDataSource()
            >>> repo = MovieRepository(data_source)
        """
        if data_source is None:
            raise ValueError("data_source não pode ser None")
        
        self.data_source = data_source
        logger.debug(f"MovieRepository inicializado com: {data_source.__class__.__name__}")

    def get_by_genre(self, genre: str, limit: int = 10) -> List[Movie]:
        """Busca filmes por gênero através da fonte de dados.
        
        Transforma dados brutos retornados por data_source.fetch_by_genre()
        em entidades Movie do domínio.
        
        Args:
            genre: Gênero do filme em português (ex: 'acao', 'comedia', 'drama')
            limit: Quantidade máxima de filmes a retornar (padrão: 10)
            
        Returns:
            Lista com até 'limit' filmes do gênero especificado,
            ordenados por rating descendente.
            Retorna lista vazia se:
            - Gênero é inválido
            - Nenhum filme foi encontrado
            - Ocorreu erro no processamento
            
        Raises:
            Nenhuma exceção é lançada (fail-safe)
            
        Example:
            >>> repo = ... # assume repositório já inicializado
            >>> filmes = repo.get_by_genre('acao', limit=5)
            >>> print(f"Encontrados {len(filmes)} filme(s)")
            Encontrados 5 filme(s)
        """
        try:
            # Valida e normaliza o gênero
            if not genre or not isinstance(genre, str):
                logger.warning(f"Gênero inválido: {genre}")
                return []
            
            genre_id = self.data_source.GENRE_MAP.get(genre.lower().strip())
            if not genre_id:
                logger.warning(
                    f"Gênero desconhecido: '{genre}'. "
                    f"Gêneros suportados: {', '.join(self.data_source.GENRE_MAP.keys())}"
                )
                return []

            logger.debug(f"Buscando filmes para gênero: '{genre}' (ID: {genre_id})")
            
            # Chama a fonte de dados (não chamada direta a TMDB)
            movies_data = self.data_source.fetch_by_genre(genre_id)
            
            if not movies_data:
                logger.info(f"Nenhum filme encontrado para gênero '{genre}'")
                return []

            movies = []
            for movie_data in movies_data[:limit]:
                try:
                    movie = Movie(
                        title=movie_data.get("title", "Sem título"),
                        genre=genre,
                        rating=float(movie_data.get("vote_average", 0.0)),
                        description=movie_data.get("overview"),
                        release_year=self._extract_year(movie_data.get("release_date"))
                    )
                    movies.append(movie)
                    
                except ValueError as e:
                    logger.warning(f"Erro ao validar filme: {movie_data.get('title', 'Desconhecido')} - {e}")
                    continue
                except (KeyError, TypeError) as e:
                    logger.warning(f"Erro ao processar dados do filme: {e}")
                    continue

            # Ordena por rating descendente
            movies.sort(key=lambda m: m.rating, reverse=True)
            
            logger.info(
                f"Repositório retornando {len(movies)} filme(s) para gênero '{genre}'"
            )
            return movies

        except Exception as e:
            logger.error(
                f"Erro crítico ao buscar filmes por gênero '{genre}': {e}",
                exc_info=True
            )
            return []
    
    def get_all(self, limit: int = 20) -> List[Movie]:
        """Busca todos os filmes disponíveis.
        
        Args:
            limit: Quantidade máxima de filmes (padrão: 20)
            
        Returns:
            Lista de filmes disponíveis
        """
        logger.debug(f"Buscando todos os filmes com limite: {limit}")
        try:
            # Implementação básica - pode ser expandida com paginação
            # Por enquanto, retorna lista vazia (usar get_by_genre)
            logger.warning("get_all não está implementado completamente")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar todos os filmes: {e}")
            return []
    
    def get_highly_rated(self, threshold: float = 7.0, limit: int = 10) -> List[Movie]:
        """Busca filmes com classificação alta.
        
        Args:
            threshold: Classificação mínima (padrão: 7.0)
            limit: Quantidade máxima de filmes (padrão: 10)
            
        Returns:
            Lista de filmes com rating >= threshold
        """
        logger.debug(f"Buscando filmes com rating >= {threshold}")
        try:
            # Implementação básica - pode ser expandida
            logger.warning("get_highly_rated não está implementado completamente")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar filmes com rating alto: {e}")
            return []
    
    @staticmethod
    def _extract_year(release_date: Optional[str]) -> Optional[int]:
        """Extrai o ano de uma data no formato YYYY-MM-DD.
        
        Args:
            release_date: Data no formato YYYY-MM-DD
            
        Returns:
            Ano como inteiro, ou None se inválido
        """
        if not release_date:
            return None
        try:
            return int(release_date.split('-')[0])
        except (IndexError, ValueError):
            return None


class MovieRepositoryFactory:
    """Factory (Fábrica) para criar instâncias de repositório.
    
    Padrão Factory centraliza a criação e configuração de repositórios
    com injeção automática de dependências.
    
    Benefícios:
    - **Centraliza a criação**: Todas as instâncias são criadas aqui
    - **Singleton Pattern**: Garante uma única instância por aplicação
    - **Desacoplamento**: Código não precisa conhecer detalhes de criação
    - **Facilita testes**: Pode ser mockado facilmente
    
    Attributes:
        _instance: Instância singleton do repositório
        _data_source: Instância singleton da fonte de dados
    
    Example:
        >>> repo = MovieRepositoryFactory.get_repository()
        >>> filmes = repo.get_by_genre('acao')
    """

    _instance: Optional[MovieRepository] = None
    _data_source: Optional[IMovieDataSource] = None

    @staticmethod
    def _get_data_source() -> IMovieDataSource:
        """Obtém ou cria a instância singleton da fonte de dados.
        
        Returns:
            Instância singleton de IMovieDataSource (atualmente TMDBDataSource)
            
        Note:
            Implementa Lazy Initialization: a fonte de dados é criada
            apenas na primeira chamada.
        """
        if MovieRepositoryFactory._data_source is None:
            logger.debug("Criando nova instância de TMDBDataSource (singleton)")
            MovieRepositoryFactory._data_source = TMDBDataSource()
            logger.info("TMDBDataSource singleton criado com sucesso")
        return MovieRepositoryFactory._data_source

    @staticmethod
    def get_repository() -> MovieRepository:
        """Retorna uma instância singleton do repositório.
        
        Cria e injeta as dependências automaticamente.
        
        Returns:
            Instância singleton de MovieRepository com todas as dependências injetadas
            
        Note:
            Implementa Singleton Pattern:
            - Primeira chamada: cria instância
            - Chamadas subsequentes: retorna mesma instância
        """
        if MovieRepositoryFactory._instance is None:
            logger.debug("Criando nova instância de MovieRepository (singleton)")
            data_source = MovieRepositoryFactory._get_data_source()
            MovieRepositoryFactory._instance = MovieRepository(data_source)
            logger.info("MovieRepository singleton criado com todas as dependências injetadas")
        return MovieRepositoryFactory._instance

    @staticmethod
    def create_new_instance(data_source: IMovieDataSource = None) -> MovieRepository:
        """Cria uma nova instância do repositório com injeção de dependência.
        
        Útil para testes onde queremos evitar estado compartilhado.
        
        Args:
            data_source: Implementação de IMovieDataSource.
                        Se None, cria uma nova TMDBDataSource
        
        Returns:
            Nova instância do MovieRepository
        """
        if data_source is None:
            data_source = TMDBDataSource()
        return MovieRepository(data_source)

    @staticmethod
    def reset():
        """Reseta as instâncias singleton (útil para testes).
        
        Example:
            >>> MovieRepositoryFactory.reset()
            >>> novo_repo = MovieRepositoryFactory.get_repository()
        """
        MovieRepositoryFactory._instance = None
        MovieRepositoryFactory._data_source = None
        logger.debug("MovieRepositoryFactory resetado")


# Instância singleton global do repositório (conveniência)
movie_repository = MovieRepositoryFactory.get_repository()
