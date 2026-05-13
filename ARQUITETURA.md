# Arquitetura do Projeto MoodFlix

Este documento descreve a arquitetura da API MoodFlix seguindo os princípios de Clean Architecture propostos por Robert C. Martin (Uncle Bob).

## 1. Visão Geral

MoodFlix é uma API REST que recomenda filmes baseado em gênero ou estado emocional (mood) do usuário, com sistema de cadastro, autenticação e MoodMaps personalizados.

A arquitetura segue Clean Architecture para garantir independência de frameworks, testabilidade, separação clara de responsabilidades e facilidade de manutenção.

## 2. Camadas

```
┌──────────────────────────────────────────────┐
│         PRESENTATION (API / Schemas)         │
│  api/v1/endpoints/movies.py                  │
│  api/v1/endpoints/user.py                    │
│  schemas/movie_schema.py                     │
│  schemas/user_schema.py                      │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│         APPLICATION (Use Cases)              │
│  recommend_movies.py                         │
│  register_user.py                            │
│  login_user.py                               │
│  add_moodmap.py                              │
│  set_default_moodmap.py                      │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│         DOMAIN (Business Logic)              │
│  entities/movie.py                           │
│  entities/user.py                            │
│  repositories/movie_repository_interface.py  │
│  repositories/user_repository_interface.py   │
│  services/mood_recommendation_service.py     │
│  services/domain_service_interface.py        │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│         INFRASTRUCTURE (Externos)            │
│  external/tmdb_data_source.py                │
│  external/tmdb_client.py                     │
│  external/mock_data.py                       │
│  repositories/movie_repository.py            │
│  repositories/memory_user_repository.py      │
└──────────────────────────────────────────────┘
```

### 2.1 Camada de Domínio

Responsabilidade: encapsular a lógica de negócio pura, sem dependências externas.

**Entidades:**

`Movie` — representa um filme. Valida que `rating` está entre 0 e 10, que `title` e `genre` não são vazios. Expõe `is_highly_rated(threshold)`.

`User` — representa um usuário. Contém `id`, `username`, `password_hash`, `moodmap_list` (máx. 5) e `default_moodmap`. Expõe `add_new_moodmap()` e `set_default_moodmap()` com validações de negócio.

**Interfaces de repositório:**

`IMovieRepository` — define `get_by_genre()`, `get_all()`, `get_highly_rated()`.

`IUserRepository` — define `get_by_id()`, `get_by_username()`, `save()`, `exists()`.

**Serviços de domínio:**

`MoodRecommendationService` — mapeia moods para gêneros e delega a busca ao repositório:

| Mood | Gênero |
|------|--------|
| feliz | comedia |
| triste | drama |
| pensativo | ficcao |
| romantico | romance |

### 2.2 Camada de Aplicação

Responsabilidade: orquestrar a lógica de negócio coordenando entidades e repositórios.

| Use Case | Descrição |
|----------|-----------|
| `recommend_movies` | Recebe `genre` ou `mood`, delega ao repositório ou ao `MoodRecommendationService` |
| `RegisterUser` | Valida unicidade do username, cria entidade `User`, persiste via repositório |
| `LoginUser` | Busca usuário por username, verifica hash da senha |
| `AddMoodMap` | Busca usuário por ID, chama `user.add_new_moodmap()`, persiste |
| `SetDefaultMoodMap` | Busca usuário por ID, chama `user.set_default_moodmap()`, persiste |

Todos os use cases recebem o repositório por injeção de dependência.

### 2.3 Camada de Apresentação

Responsabilidade: expor os use cases como endpoints HTTP.

**Endpoints implementados:**

| Método | Rota | Status |
|--------|------|--------|
| GET | `/api/v1/recommend` | ✅ Funcionando |
| GET | `/api/v1/movies` | ⚠️ Retorna lista vazia |
| POST | `/api/v1/users/register` | ✅ Funcionando |
| POST | `/api/v1/users/login` | ✅ Funcionando |
| GET | `/health` | ✅ Funcionando |

**Endpoints pendentes (use cases prontos, sem rota HTTP):**
- `POST /api/v1/users/{id}/moodmaps` — AddMoodMap
- `PATCH /api/v1/users/{id}/moodmaps/default` — SetDefaultMoodMap

### 2.4 Camada de Infraestrutura

Responsabilidade: detalhes técnicos de comunicação com sistemas externos.

**MovieRepository** — implementa `IMovieRepository`. Recebe `IMovieDataSource` por injeção. Converte dicionários da TMDB em entidades `Movie`. Usa `MovieRepositoryFactory` (Singleton).

**TMDBDataSource** — implementa `IMovieDataSource`. Mapeia nomes de gêneros em português para IDs numéricos da TMDB. Delega chamadas HTTP ao `tmdb_client`.

**MockMovieData** — dados estáticos para desenvolvimento e testes sem chave TMDB.

**MemoryUserRepository** — implementa `IUserRepository` com lista em memória. Dados perdidos ao reiniciar a aplicação. Deve ser substituído por implementação com banco de dados.

## 3. Fluxo de Dados — Recomendação por Mood

```
GET /api/v1/recommend?mood=feliz

  ↓ Endpoint (movies.py)
    Valida parâmetros

  ↓ Use Case (recommend_movies)
    Chama get_mood_recommendation_service(repository)

  ↓ MoodRecommendationService
    Mapeia "feliz" → "comedia"
    Chama repository.get_by_genre("comedia")

  ↓ MovieRepository
    Mapeia "comedia" → genre_id 35
    Chama data_source.fetch_by_genre(35)

  ↓ TMDBDataSource → tmdb_client
    GET https://api.themoviedb.org/3/discover/movie?with_genres=35

  ↑ Retorno
    List[Dict] → List[Movie] → List[MovieResponse] → JSON
```

## 4. Padrões de Design Utilizados

**Factory + Singleton** — `MovieRepositoryFactory` cria e mantém uma única instância do repositório e da fonte de dados.

**Adapter** — `TMDBDataSource` adapta a API TMDB ao contrato `IMovieDataSource`. `MovieRepository` adapta dicionários brutos em entidades `Movie`.

**Strategy** — `MoodRecommendationService` é uma estratégia de recomendação intercambiável via `IDomainService`.

**Dependency Injection** — todos os use cases e repositórios recebem suas dependências por parâmetro, nunca as instanciam diretamente.

## 5. Estado Atual e Pendências

### Implementado e funcionando
- Recomendação por gênero e por mood via TMDB
- Entidades `Movie` e `User` com validações de negócio
- Use cases de usuário completos (registro, login, moodmap)
- Repositório de usuários em memória

### Pendente / incompleto
- `GET /movies` retorna lista vazia
- Hash de senha usa prefixo simples (`hashed_`), não é seguro para produção
- Endpoints de MoodMap não expostos via HTTP
- MoodMap do usuário não influencia o `/recommend`
- Sem autenticação JWT
- Sem banco de dados persistente
- Sem testes automatizados com pytest

## 6. Como Estender o Projeto

### Adicionar novo tipo de recomendação
1. Criar nova classe que implemente `IDomainService` em `domain/services/`
2. Criar ou adaptar o use case em `application/use_cases/`
3. Expor novo endpoint em `api/v1/endpoints/`

### Trocar fonte de dados
Implementar `IMovieDataSource` com a nova fonte e alterar `MovieRepositoryFactory._get_data_source()`. Nenhuma outra camada precisa mudar.

### Adicionar banco de dados
Implementar `IUserRepository` (e futuramente `IMovieRepository`) com SQLAlchemy ou similar. Substituir `MemoryUserRepository` na instanciação em `user.py`.

### Adicionar autenticação JWT
1. Instalar `python-jose` e `passlib`
2. Gerar token no `LoginUser` use case
3. Criar middleware ou dependency do FastAPI para validar token
4. Proteger endpoints de MoodMap e recomendações personalizadas

## 7. Dependências entre Camadas

```
Domain        ← não depende de nada externo
Application   ← depende apenas de interfaces do Domain
Presentation  ← depende de Application e Schemas
Infrastructure← implementa interfaces do Domain
```

A regra fundamental: **camadas internas nunca importam de camadas externas**.

---

Documentação atualizada em: maio/2026
Arquitetura: Clean Architecture (Robert C. Martin)
Framework: FastAPI 0.135
Python: 3.8+
