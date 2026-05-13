# Guia de Início Rápido — MoodFlix API

## 1. Instalação

```bash
# Passo 1: Acessar a pasta do projeto
cd moodflix-main

# Passo 2: Criar ambiente virtual
python -m venv venv

# Passo 3: Ativar ambiente (Windows)
venv\Scripts\activate
# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Passo 4: Instalar dependências
pip install -r requirements.txt

# Passo 5: Criar arquivo .env
cp .env.example .env
# Editar .env e adicionar sua TMDB_API_KEY
# Obter em: https://www.themoviedb.org/settings/api
```

## 2. Executar a Aplicação

```bash
# Opção 1: Python direto
python app/main.py

# Opção 2: Uvicorn com reload automático
uvicorn app.main:app --reload --port 8000
```

Saída esperada:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: MoodFlix API v1.0.0 iniciada
INFO: Documentacao disponivel em: /docs
```

## 3. Acessar

| URL | Descrição |
|-----|-----------|
| http://localhost:8000 | API |
| http://localhost:8000/docs | Swagger (recomendado para testar) |
| http://localhost:8000/redoc | ReDoc |
| http://localhost:8000/health | Health check |

## 4. Testar os Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```
```json
{"status": "healthy", "app": "MoodFlix API"}
```

### Recomendação por Gênero
```bash
curl "http://localhost:8000/api/v1/recommend?genre=acao"
curl "http://localhost:8000/api/v1/recommend?genre=comedia"
curl "http://localhost:8000/api/v1/recommend?genre=ficcao"
```

Gêneros disponíveis: `acao`, `comedia`, `drama`, `ficcao`, `romance`, `animacao`, `terror`

### Recomendação por Mood
```bash
curl "http://localhost:8000/api/v1/recommend?mood=feliz"
curl "http://localhost:8000/api/v1/recommend?mood=triste"
```

Moods disponíveis: `feliz`, `triste`, `pensativo`, `romantico`

### Cadastrar Usuário
```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

## 5. Executar os Testes Manuais

```bash
# Testa cadastro e duplicidade de usuário
python test_register.py

# Testa fluxo completo: cadastro, login, MoodMap, limite de 5 mapas
python test_user_flow.py
```

## 6. Estrutura do Projeto

```
moodflix-main/
├── README.md                   ← Documentação principal
├── ARQUITETURA.md              ← Design e padrões do projeto
├── GUIA_INICIO_RAPIDO.md       ← Este arquivo
├── requirements.txt
├── test_register.py            ← Teste manual de cadastro
├── test_user_flow.py           ← Teste manual de fluxo completo
│
└── app/
    ├── config.py               ← Variáveis de ambiente
    ├── main.py                 ← Entrada da aplicação FastAPI
    │
    ├── domain/                 ← Lógica de negócio pura
    │   ├── entities/           ← Movie, User
    │   ├── repositories/       ← Interfaces IMovieRepository, IUserRepository
    │   └── services/           ← MoodRecommendationService
    │
    ├── application/            ← Casos de uso
    │   └── use_cases/          ← recommend_movies, register_user, login_user,
    │                               add_moodmap, set_default_moodmap
    │
    ├── api/                    ← Endpoints HTTP
    │   └── v1/endpoints/       ← movies.py, user.py
    │
    ├── infrastructure/         ← Detalhes técnicos
    │   └── external/           ← TMDBDataSource, tmdb_client, mock_data
    │
    ├── repositories/           ← MovieRepository, MemoryUserRepository
    └── schemas/                ← MovieResponse, UserCreate, UserResponse
```

## 7. Variáveis de Ambiente

```env
TMDB_API_KEY=sua_chave_aqui     # obrigatório
APP_NAME=MoodFlix API           # opcional
APP_VERSION=1.0.0               # opcional
LOG_LEVEL=INFO                  # opcional (DEBUG, INFO, WARNING, ERROR)
DEBUG=False                     # opcional
```

## 8. O que Está Funcionando Hoje

| Funcionalidade | Status |
|----------------|--------|
| Recomendar por gênero | ✅ |
| Recomendar por mood | ✅ |
| Cadastrar usuário | ✅ |
| Login de usuário | ✅ |
| Listar filmes (`/movies`) | ⚠️ Retorna lista vazia |
| Endpoints de MoodMap | ⚠️ Use cases prontos, sem rota HTTP |
| Autenticação JWT | ❌ Pendente |
| Banco de dados persistente | ❌ Tudo em memória |

## 9. Problemas Comuns

**"No module named 'app'"**
Verifique se está na pasta raiz do projeto (`moodflix-main`) antes de executar.

**"TMDB_API_KEY not found" ou ValidationError**
Crie o arquivo `.env` com a chave. Veja a seção de variáveis de ambiente acima.

**"Connection refused"**
A aplicação não está rodando. Execute `python app/main.py` primeiro.

**Recomendação retorna lista vazia**
Verifique se a `TMDB_API_KEY` no `.env` é válida. Teste o health check primeiro.

## 10. Recursos Úteis

- Documentação FastAPI: https://fastapi.tiangolo.com/
- Documentação Pydantic: https://docs.pydantic.dev/
- API TMDB: https://www.themoviedb.org/settings/api
- Clean Architecture: Robert C. Martin — "Clean Architecture: A Craftsman's Guide"
