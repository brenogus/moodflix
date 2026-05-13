# MoodFlix API

API REST de recomendação de filmes baseada em gênero e estado emocional (mood), com sistema de usuários e MoodMaps personalizados.

## Início Rápido

### Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# Editar .env e adicionar sua chave TMDB_API_KEY
```

### Executar

```bash
python app/main.py
```

Acesse:
- API: `http://localhost:8000`
- Documentação Swagger: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`

## API Endpoints

### Filmes

#### GET /api/v1/recommend
Recomenda filmes baseado em gênero ou mood.

**Query Parameters:**
- `genre`: (opcional) `acao`, `comedia`, `drama`, `ficcao`, `romance`, `animacao`, `terror`
- `mood`: (opcional) `triste`, `feliz`, `pensativo`, `romantico`

**Mapeamento de Mood → Gênero:**
| Mood | Gênero |
|------|--------|
| feliz | comedia |
| triste | drama |
| pensativo | ficcao |
| romantico | romance |

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/recommend?genre=acao"
curl "http://localhost:8000/api/v1/recommend?mood=feliz"
```

**Response:**
```json
[
  {
    "title": "Interestelar",
    "genre": "ficcao",
    "rating": 8.6,
    "description": "Um filme sobre viagens espaciais",
    "release_year": 2014
  }
]
```

#### GET /api/v1/movies
Lista filmes disponíveis. ⚠️ **Não implementado** — retorna lista vazia.

**Query Parameters:**
- `limit`: Quantidade de filmes (1-100, padrão: 20)

### Usuários

#### POST /api/v1/users/register
Cadastra um novo usuário.

**Body:**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Response:**
```json
{
  "id": "uuid-gerado",
  "username": "seu_usuario",
  "message": "Usuário cadastrado com sucesso!"
}
```

#### POST /api/v1/users/login
Autentica um usuário existente.

**Body:**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Response:**
```json
{
  "id": "uuid-gerado",
  "username": "seu_usuario",
  "message": "Login realizado com sucesso!"
}
```

## Sistema de MoodMaps

MoodMaps são perfis de preferência de humor criados por cada usuário. Cada usuário pode ter até **5 MoodMaps** e definir um como padrão.

Um MoodMap é um dicionário com campos livres, por exemplo:
```json
{
  "moodmap_id": "map_001",
  "name": "Foco Total",
  "genre": "ficcao"
}
```

> ⚠️ Os endpoints de MoodMap ainda não estão expostos via API HTTP. A lógica existe nos use cases (`AddMoodMap`, `SetDefaultMoodMap`) mas aguarda integração com autenticação JWT.

## Arquitetura

O projeto segue **Clean Architecture** com 4 camadas bem definidas:

```
Presentation (API) → Application (Use Cases) → Domain (Business Logic) → Infrastructure (External)
```

Para detalhes completos, consulte [ARQUITETURA.md](./ARQUITETURA.md).

### Estrutura de Diretórios

```
app/
├── domain/
│   ├── entities/           # Movie, User
│   ├── repositories/       # IMovieRepository, IUserRepository
│   └── services/           # IDomainService, MoodRecommendationService
├── application/
│   └── use_cases/          # recommend_movies, register_user, login_user,
│                           # add_moodmap, set_default_moodmap
├── api/
│   └── v1/endpoints/       # movies.py, user.py
├── infrastructure/
│   ├── external/           # TMDBDataSource, tmdb_client, mock_data
│   └── db/                 # (reservado para banco de dados futuro)
├── repositories/           # MovieRepository, MemoryUserRepository
├── schemas/                # MovieResponse, UserCreate, UserLogin, UserResponse
└── config.py               # Configurações via pydantic-settings
```

## Variáveis de Ambiente

Criar arquivo `.env`:

```env
TMDB_API_KEY=sua_chave_api_aqui
APP_NAME=MoodFlix API
APP_VERSION=1.0.0
LOG_LEVEL=INFO
DEBUG=False
```

Obter chave TMDB em: https://www.themoviedb.org/settings/api

## Dependências

- **FastAPI** — Framework web
- **Pydantic / pydantic-settings** — Validação de dados e variáveis de ambiente
- **requests** — Cliente HTTP para a API TMDB
- **python-dotenv** — Carregamento do arquivo `.env`
- **uvicorn** — Servidor ASGI

Ver `requirements.txt` para versões completas.

## Testes

O projeto possui scripts de teste manual em:
- `test_register.py` — Testa cadastro e duplicidade de usuário
- `test_user_flow.py` — Testa fluxo completo: cadastro, login, MoodMap e limite de 5 mapas

```bash
python test_register.py
python test_user_flow.py
```

> Testes automatizados com `pytest` ainda não implementados.

## Estado Atual e Próximos Passos

### ✅ Implementado
- Recomendação de filmes por gênero (via API TMDB)
- Recomendação de filmes por mood (mood → gênero → TMDB)
- Cadastro e login de usuário (repositório em memória)
- Entidade User com MoodMaps (lógica de domínio completa)
- Use cases: RegisterUser, LoginUser, AddMoodMap, SetDefaultMoodMap

### ⚠️ Parcialmente implementado
- `GET /movies` — endpoint existe mas retorna lista vazia
- Hash de senha — implementado com prefixo simples (`hashed_`), não seguro para produção
- MoodMaps — lógica completa, mas endpoints HTTP não expostos

### 🔜 Próximos passos prioritários
1. **Hash de senha seguro** — substituir por `bcrypt` ou `passlib`
2. **Autenticação JWT** — proteger endpoints e gerar tokens no login
3. **Expor endpoints de MoodMap** — conectar use cases já prontos à API
4. **Conectar MoodMap ao `/recommend`** — usar preferências do usuário nas recomendações
5. **Banco de dados persistente** — substituir `MemoryUserRepository` por SQLite/PostgreSQL
6. **Testes automatizados** — implementar suite com `pytest`

## Princípios Aplicados

- **Dependency Injection** — Use cases recebem repositórios como parâmetro
- **SOLID** — Princípios aplicados em todas as camadas
- **Fail-Safe** — Endpoints retornam lista vazia em caso de erro, nunca quebram
- **Logging** — Logging estruturado em todas as camadas

## Autor

Breno Gustavo de Oliveira e Ferreira

## Suporte

Para documentação detalhada da arquitetura: [ARQUITETURA.md](./ARQUITETURA.md)
Para guia de início rápido: [GUIA_INICIO_RAPIDO.md](./GUIA_INICIO_RAPIDO.md)
