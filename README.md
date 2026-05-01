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
│   ├── entities/        # Modelos de domínio
│   ├── repositories/    # Interfaces de repositório
│   └── services/        # Serviços de domínio
├── aplication/          # Casos de uso
│   └── use_cases/       
├── api/                 # Endpoints HTTP
│   └── v1/endpoints/
├── infrastructure/      # Detalhes técnicos
│   ├── external/        # APIs externas (TMDB)
│   └── db/              # Banco de dados
├── schemas/             # DTOs Pydantic
└── utils/               # Funções auxiliares
```

##  Variáveis de Ambiente

Criar arquivo `.env`:

```env
TMDB_API_KEY=sua_chave_api_aqui
APP_NAME=MoodFlix API
APP_VERSION=1.0.0
LOG_LEVEL=INFO
DEBUG=False
```

##  Dependências

- **FastAPI**: Framework web
- **Pydantic**: Validação de dados
- **requests**: Cliente HTTP
- **python-dotenv**: Variáveis de ambiente

Ver `requirements.txt` para versões completas.

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

1. Autenticação com JWT
2. Banco de dados persistente (PostgreSQL)
3. Cache com Redis
4. Testes unitários e integração
5. Docker containerização
6. CI/CD pipeline
7. Monitoramento e alertas
8. Rate limiting

##  Licença


##  Autor

Breno Gustavo de Oliveira e Ferreira

##  Suporte

Para documentação detalhada da arquitetura: [ARQUITETURA.md](./ARQUITETURA.md)
