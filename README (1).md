# MoodFlix API

API REST de recomendação de filmes baseada em gênero e estado emocional (mood).

##  Início Rápido

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
# Editar .env e adicionar suas chaves
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

##  API Endpoints

### GET /api/v1/recommend

Recomenda filmes baseado em gênero ou mood.

**Query Parameters:**
- `genre`: (opcional) `acao`, `comedia`, `drama`, `ficcao`, `romance`, `animacao`, `terror`
- `mood`: (opcional) `triste`, `feliz`, `pensativo`, `romantico`

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

---

### POST /api/v1/users/register

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
  "message": "Usuário cadastrado com sucesso!",
  "token": null
}
```

---

### POST /api/v1/users/login

Autentica o usuário e retorna um token JWT.

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
  "id": "uuid-do-usuario",
  "username": "seu_usuario",
  "message": "Login realizado com sucesso!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### POST /api/v1/users/logout

Invalida o token JWT do usuário (logoff real via blacklist).

**Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "message": "Token adicionado na blacklist com sucesso."
}
```

---

##  Arquitetura

O projeto segue **Clean Architecture**:

```
Presentation (API) → Application (Use Cases) → Domain (Business Logic) → Infrastructure (External)
```

Para detalhes completos, consulte [ARQUITETURA.md](./ARQUITETURA.md).

### Estrutura de Diretórios

```
app/
├── domain/              # Lógica de negócio pura
│   ├── entities/        # Modelos de domínio (Movie, User)
│   ├── repositories/    # Interfaces de repositório
│   └── services/        # Serviços de domínio (token, mood)
├── application/         # Casos de uso
│   └── use_cases/       # register, login, logout, recommend, moodmap
├── api/                 # Endpoints HTTP
│   └── v1/endpoints/    # movies.py, user.py
├── infrastructure/      # Detalhes técnicos
│   ├── external/        # APIs externas (TMDB)
│   └── db/              # Banco de dados
├── repositories/        # Implementações concretas em memória
├── schemas/             # DTOs Pydantic
└── utils/               # Funções auxiliares
```

##  Variáveis de Ambiente

Criar arquivo `.env`:

```env
TMDB_API_KEY=sua_chave_api_aqui
SECRET_KEY=sua_chave_secreta_jwt_aqui
APP_NAME=MoodFlix API
APP_VERSION=1.0.0
LOG_LEVEL=INFO
DEBUG=False
```

Para gerar uma `SECRET_KEY` segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

##  Dependências

- **FastAPI**: Framework web
- **Pydantic**: Validação de dados
- **PyJWT**: Geração e verificação de tokens JWT
- **requests**: Cliente HTTP
- **python-dotenv**: Variáveis de ambiente

Ver `requirements.txt` para versões completas.

##  Autenticação JWT

O projeto implementa autenticação stateless com JWT e logoff real via blacklist.

**Fluxo:**
1. `POST /register` → cria o usuário
2. `POST /login` → retorna token JWT (validade: 24h)
3. Use o token nas requisições protegidas
4. `POST /logout` → invalida o token na blacklist

**Estratégia de blacklist:**
- Apenas tokens invalidados por logoff são armazenados
- Tokens expirados são removidos automaticamente da blacklist
- A blacklist nunca cresce infinitamente

##  Testes

```bash
pip install pytest
pytest tests/
```

##  Princípios Aplicados

-  **Dependency Injection**: Injeção de dependências em todos os níveis
-  **SOLID**: Princípios SOLID respeitados
-  **Clean Code**: Código limpo e bem documentado
-  **Fail-Safe**: Aplicação retorna dados seguros em caso de erro
-  **Logging**: Logging estruturado e informativo

##  Próximos Passos

1. ~~Autenticação com JWT~~ ✅
2. Middleware de proteção de rotas
3. Banco de dados persistente (PostgreSQL)
4. Cache com Redis
5. Refresh token
6. Testes unitários e integração
7. Docker containerização
8. CI/CD pipeline
9. Monitoramento e alertas
10. Rate limiting

##  Licença


##  Autor

Breno Gustavo de Oliveira e Ferreira

##  Suporte

Para documentação detalhada da arquitetura: [ARQUITETURA.md](./ARQUITETURA.md)
