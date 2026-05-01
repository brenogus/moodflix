"""
ARQUITETURA DO PROJETO MOODFLIX
================================

Este documento detalha a arquitetura da API MoodFlix seguindo os princípios
de Clean Architecture proposta por Robert C. Martin (Uncle Bob).

## 1. VISÃO GERAL

MoodFlix é uma API REST que recomenda filmes baseado em gênero ou estado emocional
(mood) do usuário. A arquitetura segue Clean Architecture para garantir:
- Independência de frameworks
- Testabilidade
- Separação clara de responsabilidades
- Facilidade de manutenção


## 2. ESTRUTURA DE CAMADAS

A aplicação está organizada em camadas concêntricas, onde as camadas internas
não conhecem as camadas externas:

```
┌─────────────────────────────────────────────────┐
│           CAMADA DE APRESENTAÇÃO (UI/API)        │
│  - endpoints/ (rotas HTTP)                      │
│  - schemas/ (DTOs - Data Transfer Objects)      │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│           CAMADA DE APLICAÇÃO (Use Cases)        │
│  - use_cases/ (orquestração de lógica)          │
│  - Depende APENAS de abstrações do domínio      │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│        CAMADA DE DOMÍNIO (Business Logic)        │
│  - entities/ (modelos de negócio)               │
│  - repositories/ (interfaces)                    │
│  - services/ (lógica de domínio complexa)       │
│  - Sem dependências externas                    │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│       CAMADA DE INFRAESTRUTURA (Externos)        │
│  - external/ (APIs, bancos de dados)             │
│  - db/ (configurações de banco)                  │
│  - repositories/ (implementações concretas)      │
└─────────────────────────────────────────────────┘
```

### 2.1 CAMADA DE DOMÍNIO (app/domain/)

**Responsabilidade**: Encapsular a lógica de negócio pura

**Arquivos**:
- `entities/movie.py`: Entidade Movie que representa um filme
- `repositories/movie_repository_interface.py`: Interface que define contrato
- `services/domain_service_interface.py`: Interface para serviços
- `services/mood_recommendation_service.py`: Serviço de recomendação por mood

**Características**:
- Não tem dependências de frameworks externos
- Contém validações de negócio
- Defini contralos através de interfaces (ABC)
- Implementa inversão de dependência

**Exemplo - Entidade Movie**:
```python
@dataclass
class Movie:
    title: str
    genre: str
    rating: float
    
    def __post_init__(self):
        # Validação de negócio
        if not (0.0 <= self.rating <= 10.0):
            raise ValueError("Rating deve estar entre 0 e 10")
```

### 2.2 CAMADA DE APLICAÇÃO (app/aplication/)

**Responsabilidade**: Orquestrar a lógica de negócio e coordenar entidades

**Arquivos**:
- `use_cases/recommend_movies.py`: Caso de uso de recomendação

**Características**:
- Implementa Use Cases (casos de uso da aplicação)
- Usa Dependency Injection para receber repositórios e serviços
- Não contém lógica de validação complexa (deixa para domínio)
- Coordena chamadas entre entidades de domínio

**Exemplo - Use Case**:
```python
def recommend_movies(
    repository: IMovieRepository,  # Injeção de dependência
    genre: Optional[str] = None,
    mood: Optional[str] = None
) -> List[Movie]:
    if genre:
        return repository.get_by_genre(genre)
    elif mood:
        service = get_mood_recommendation_service()
        return service.get_recommendations(mood=mood)
    return []
```

### 2.3 CAMADA DE APRESENTAÇÃO (app/api/)

**Responsabilidade**: Expor os use cases como endpoints HTTP

**Arquivos**:
- `api/v1/endpoints/movies.py`: Endpoints HTTP
- `schemas/movie_schema.py`: DTOs Pydantic para API

**Características**:
- Define rotas HTTP (GET, POST, etc.)
- Valida entrada com Pydantic
- Transforma entidades de domínio em DTOs
- Trata erros HTTP
- Dependência mínima de frameworks

**Exemplo - Endpoint**:
```python
@router.get("/recommend", response_model=List[MovieResponse])
def recommend(
    genre: Optional[str] = Query(None),
    mood: Optional[str] = Query(None)
):
    movies = recommend_movies(
        repository=movie_repository,
        genre=genre,
        mood=mood
    )
    return [MovieResponse.from_movie(m) for m in movies]
```

### 2.4 CAMADA DE INFRAESTRUTURA (app/infrastructure/)

**Responsabilidade**: Detalhes técnicos de comunicação com sistemas externos

**Arquivos**:
- `external/movie_data_source_interface.py`: Interface para fonte de dados
- `external/tmdb_data_source.py`: Implementação usando API TMDB
- `external/tmdb_client.py`: Cliente HTTP para TMDB
- `db/database.py`: Configuração de banco de dados

**Características**:
- Implementa interfaces definidas no domínio
- Adapta APIs externas ao formato esperado
- Pode ser substituída facilmente (MockDataSource para testes)
- Exemplo de Adapter Pattern

**Exemplo - Data Source TMDB**:
```python
class TMDBDataSource(IMovieDataSource):
    def fetch_by_genre(self, genre_id: int) -> List[Dict]:
        # Implementação específica de TMDB
        response = requests.get(f"https://api.tmdb.org/...{genre_id}")
        return response.json()["results"]
```

### 2.5 CAMADA DE CONFIGURAÇÃO (app/config.py)

**Responsabilidade**: Gerenciar variáveis de ambiente e configurações

**Características**:
- Usa Pydantic Settings
- Carrega de arquivo .env
- Centralizado em um único lugar
- Type-safe com validação


## 3. PRINCÍPIOS APLICADOS

### 3.1 DEPENDENCY INJECTION (DI)

A aplicação usa injeção de dependências para desacoplar componentes:

```
┌──────────────────┐
│  Endpoint        │
│  - recebe repo   │──┐
└──────────────────┘  │
                      │ Injeção
┌──────────────────┐  │
│  Use Case        │◄─┤
│  - recebe repo   │  │
└──────────────────┘  │
                      │
┌──────────────────┐  │
│  Repository      │◄─┘
│  - implementa    │
│    interface     │
└──────────────────┘
```

**Factory Pattern** para criar instâncias:
```python
class MovieRepositoryFactory:
    @staticmethod
    def get_repository() -> MovieRepository:
        # Singleton: mesma instância sempre retornada
        return MovieRepositoryFactory._instance
```

### 3.2 INVERSÃO DE DEPENDÊNCIA (Dependency Inversion Principle)

Módulos dependem de abstrações, não de implementações concretas:

```
✓ BOM:
  Use Case → IMovieRepository (interface)
  ↓
  TMDBDataSource (implementação)

✗ RUIM:
  Use Case → TMDBDataSource (acoplado)
```

### 3.3 SINGLE RESPONSIBILITY PRINCIPLE (SRP)

Cada classe tem uma única responsabilidade:

| Classe | Responsabilidade |
|--------|------------------|
| Movie | Encapsular dados de um filme |
| MovieRepository | Transformar dados em entidades |
| recommend_movies() | Orquestrar recomendação |
| recommend() endpoint | Expor como HTTP |

### 3.4 OPEN/CLOSED PRINCIPLE (OCP)

Aberto para extensão, fechado para modificação:

- Adicionar novo tipo de recomendação? → Estender IDomainService
- Adicionar novo endpoint? → Criar novo route
- Trocar TMDB por outro serviço? → Implementar IMovieDataSource

### 3.5 LISKOV SUBSTITUTION PRINCIPLE (LSP)

Implementações podem ser substituídas sem quebrar o código:

```python
# Qualquer implementação de IMovieDataSource funciona:
data_source = TMDBDataSource()          # Produção
data_source = MockDataSource()          # Testes
data_source = DatabaseDataSource()      # Futuro
repo = MovieRepository(data_source)     # Funciona igual!
```

### 3.6 INTERFACE SEGREGATION PRINCIPLE (ISP)

Interfaces específicas e pequenas:

```python
class IMovieRepository(ABC):
    # Interface específica para repositório
    def get_by_genre(self, genre: str) -> List[Movie]: pass

class IMovieDataSource(ABC):
    # Interface específica para fonte de dados
    def fetch_by_genre(self, genre_id: int) -> List[Dict]: pass
```


## 4. FLUXO DE DADOS

### 4.1 Requisição HTTP

```
1. GET /api/v1/recommend?genre=acao

   ↓

2. Endpoint movies.recommend(genre="acao")
   - Valida parametros com Query
   
   ↓

3. Chama recommend_movies(repository=repo, genre="acao")
   - Use case: orquestra lógica
   
   ↓

4. repository.get_by_genre("acao")
   - Repositório: transforma dados
   
   ↓

5. data_source.fetch_by_genre(28)
   - Data Source: chama API TMDB
   
   ↓

6. requests.get("https://api.tmdb.org/...")
   - Cliente HTTP: chamada externa
   
   ↓

7. Resposta volta transformada:
   Lista[Movie] → List[MovieResponse] → JSON

8. HTTP 200 OK com JSON
```

### 4.2 Transformação de Dados

```
TMDB API Response (Dict)
    ↓
TMDBDataSource.fetch_by_genre()
    ↓ (Adapter)
MovieRepository.get_by_genre()
    ↓ (Mapper: Dict → Movie)
Movie (Entidade de Domínio)
    ↓
use_cases.recommend_movies()
    ↓
MovieResponse (DTO)
    ↓
JSON na resposta HTTP
```


## 5. PADRÕES DE DESIGN

### 5.1 Factory Pattern

```python
# MovieRepositoryFactory cria instâncias do repositório
repo = MovieRepositoryFactory.get_repository()

# Benefícios:
# - Centraliza criação
# - Gerencia singleton
# - Facilita testes
```

### 5.2 Adapter Pattern

```python
# TMDBDataSource adapta API TMDB ao contrato IMovieDataSource
class TMDBDataSource(IMovieDataSource):
    def fetch_by_genre(self, genre_id: int) -> List[Dict]:
        # Adapta chamada à API
        response = fetch_movies_by_genre(genre_id)
        return response
```

### 5.3 Singleton Pattern

```python
# Instância única de MovieRepository
_instance = None

@staticmethod
def get_repository() -> MovieRepository:
    if _instance is None:
        _instance = MovieRepository(data_source)
    return _instance
```

### 5.4 Strategy Pattern

```python
# Diferentes estratégias de recomendação
mood_service = MoodRecommendationService()  # Strategy 1
# Future: GenreService, UserPreferenceService  # Strategy 2, 3
```


## 6. ESTRUTURA DE DIRETÓRIOS

```
moodflix-main/
│
├── app/
│   ├── __init__.py
│   │
│   ├── config.py                    # Configurações
│   ├── main.py                      # Aplicação principal
│   │
│   ├── domain/                      # CAMADA DE DOMÍNIO
│   │   ├── entities/
│   │   │   └── movie.py            # Entidade Movie
│   │   ├── repositories/
│   │   │   └── movie_repository_interface.py  # Interface
│   │   └── services/
│   │       ├── domain_service_interface.py    # Interface
│   │       └── mood_recommendation_service.py # Implementação
│   │
│   ├── aplication/                 # CAMADA DE APLICAÇÃO
│   │   └── use_cases/
│   │       └── recommend_movies.py  # Use Case
│   │
│   ├── api/                        # CAMADA DE APRESENTAÇÃO
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           └── movies.py       # Endpoints HTTP
│   │
│   ├── schemas/                    # DTOs da API
│   │   └── movie_schema.py
│   │
│   ├── infrastructure/             # CAMADA DE INFRAESTRUTURA
│   │   ├── db/
│   │   │   └── database.py
│   │   ├── repositories/
│   │   │   └── movie_repository.py  # Implementação concreta
│   │   └── external/
│   │       ├── movie_data_source_interface.py  # Interface
│   │       ├── tmdb_data_source.py   # Implementação TMDB
│   │       ├── tmdb_client.py        # Cliente HTTP
│   │       └── mock_data.py          # Dados para testes
│   │
│   └── utils/
│       └── helpers.py              # Funções auxiliares
│
├── requirements.txt                # Dependências Python
└── .env                           # Variáveis de ambiente
```


## 7. DEPENDÊNCIAS DO PROJETO

**Framework Web**: FastAPI
- Para criar endpoints HTTP
- Validação automática com Pydantic
- Documentação automática (Swagger)

**Cliente HTTP**: requests
- Para chamar API TMDB

**Configuração**: pydantic-settings
- Para gerenciar variáveis de ambiente

**Banco de Dados** (futuro): SQLAlchemy
- Para persistência de dados


## 8. COMO ADICIONAR NOVAS FUNCIONALIDADES

### 8.1 Novo Endpoint de Recomendação

1. Criar nova interface em `domain/services/`:
```python
class INewRecommendationService(IDomainService):
    def get_recommendations(self, **kwargs) -> List[Movie]: pass
```

2. Implementar serviço em `domain/services/`:
```python
class NewRecommendationService(INewRecommendationService):
    def get_recommendations(self, **kwargs) -> List[Movie]:
        # Implementação
        pass
```

3. Usar em use case `aplication/use_cases/`:
```python
def recommend_movies_by_new_criteria(...):
    service = NewRecommendationService()
    return service.get_recommendations()
```

4. Expor como endpoint em `api/v1/endpoints/`:
```python
@router.get("/recommend-new")
def recommend_new(...):
    movies = recommend_movies_by_new_criteria(...)
    return [MovieResponse.from_movie(m) for m in movies]
```

### 8.2 Adicionar Banco de Dados

1. Implementar `IMovieRepository` com banco de dados:
```python
class DatabaseMovieRepository(IMovieRepository):
    def get_by_genre(self, genre: str) -> List[Movie]:
        # Query no banco
        results = db.session.query(MovieModel).filter(...)
        return [Movie.from_model(r) for r in results]
```

2. Alterar factory para usar nova implementação:
```python
@staticmethod
def _get_data_source():
    return DatabaseDataSource()
```

### 8.3 Adicionar Testes

```python
# tests/test_recommend_movies.py
from unittest.mock import Mock
from app.aplication.use_cases.recommend_movies import recommend_movies

def test_recommend_by_genre():
    mock_repo = Mock(spec=IMovieRepository)
    mock_repo.get_by_genre.return_value = [...]
    
    result = recommend_movies(repository=mock_repo, genre="acao")
    
    assert len(result) > 0
    mock_repo.get_by_genre.assert_called_once_with("acao", limit=10)
```


## 9. VANTAGENS DA CLEAN ARCHITECTURE

| Vantagem | Benefício |
|----------|-----------|
| **Testabilidade** | Mock de dependências é fácil |
| **Flexibilidade** | Trocar implementações sem modificar código |
| **Manutenibilidade** | Cada camada tem responsabilidade clara |
| **Escalabilidade** | Fácil adicionar novas funcionalidades |
| **Independência** | Código não acoplado a frameworks |
| **Documentação** | Estrutura é auto-documentada |
| **Equipes** | Desenvolvedores trabalham em paralelo |
| **Refactoring** | Seguro refatorar sem quebrar funcionalidades |


## 10. PRÓXIMOS PASSOS

1. **Banco de Dados**: Implementar com SQLAlchemy
2. **Autenticação**: JWT tokens
3. **Cache**: Redis para filmes populares
4. **Paginação**: Suporte a offset/limit
5. **Filtros**: Filtros avançados de filmes
6. **Testes**: Suite completa com pytest
7. **CI/CD**: GitHub Actions
8. **Containerização**: Docker
9. **API Versioning**: Suporte a múltiplas versões
10. **Monitoring**: Logs e métricas


## CONCLUSÃO

A arquitetura MoodFlix segue rigorosamente os princípios de Clean Architecture,
garantindo um código:
- Independente de detalhes técnicos
- Fácil de testar
- Flexível para mudanças
- Bem organizado
- Pronto para crescer

Para dúvidas, consulte a documentação das classes individuais (docstrings)
e os exemplos de uso nos endpoints.

---
Documentação gerada em: maio/2026
Arquitetura: Clean Architecture (Robert C. Martin)
Framework: FastAPI
Python: 3.8+
"""
