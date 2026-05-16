# ARQUITETURA DO PROJETO MOODFLIX

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
- `entities/user.py`: Entidade User que representa um usuário
- `repositories/movie_repository_interface.py`: Contrato para repositório de filmes
- `repositories/user_repository_interface.py`: Contrato para repositório de usuários
- `repositories/blacklist_repository_interface.py`: Contrato para repositório de blacklist JWT
- `services/domain_service_interface.py`: Interface para serviços
- `services/mood_recommendation_service.py`: Serviço de recomendação por mood
- `services/token_service.py`: Serviço de geração, verificação e invalidação de tokens JWT

**Características**:
- Não tem dependências de frameworks externos
- Contém validações de negócio
- Define contratos através de interfaces (ABC)
- Implementa inversão de dependência

**Exemplo - Entidade User**:
```python
@dataclass
class User:
    id: str
    username: str
    password_hash: str
    moodmap_list: List[Dict[str, str]]
    default_moodmap: Optional[Dict[str, str]]

    def add_new_moodmap(self, moodmap):
        if len(self.moodmap_list) >= 5:
            raise ValueError("Limite de 5 moodmaps atingido")
        self.moodmap_list.append(moodmap)
```

### 2.2 CAMADA DE APLICAÇÃO (app/application/)

**Responsabilidade**: Orquestrar a lógica de negócio e coordenar entidades

**Arquivos**:
- `use_cases/recommend_movies.py`: Recomendação de filmes
- `use_cases/register_user.py`: Cadastro de usuário
- `use_cases/login_user.py`: Autenticação e geração de token JWT
- `use_cases/logout_user.py`: Invalidação de token via blacklist
- `use_cases/add_moodmap.py`: Adição de moodmap ao usuário
- `use_cases/set_default_moodmap.py`: Definição de moodmap padrão

**Características**:
- Implementa Use Cases (casos de uso da aplicação)
- Usa Dependency Injection para receber repositórios e serviços
- Não contém lógica de validação complexa (delega ao domínio)
- Coordena chamadas entre entidades de domínio

**Exemplo - Use Case de Login**:
```python
class LoginUser:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, login_data: Dict) -> Dict:
        user = self.user_repository.get_by_username(login_data["username"])
        # verifica senha...
        token = create_token(user)
        return {"id": user.id, "username": user.username, "token": token}
```

### 2.3 CAMADA DE APRESENTAÇÃO (app/api/)

**Responsabilidade**: Expor os use cases como endpoints HTTP

**Arquivos**:
- `api/v1/endpoints/movies.py`: Endpoints de filmes e recomendações
- `api/v1/endpoints/user.py`: Endpoints de usuários (register, login, logout)
- `schemas/movie_schema.py`: DTOs de filmes
- `schemas/user_schema.py`: DTOs de usuários (UserCreate, UserLogin, UserResponse, UserLogout, UserLogoutResponse)

**Características**:
- Define rotas HTTP (GET, POST, etc.)
- Valida entrada com Pydantic
- Transforma entidades de domínio em DTOs
- Trata erros HTTP
- Dependência mínima de frameworks

### 2.4 CAMADA DE INFRAESTRUTURA (app/infrastructure/ e app/repositories/)

**Responsabilidade**: Detalhes técnicos de comunicação com sistemas externos e persistência

**Arquivos**:
- `infrastructure/external/tmdb_data_source.py`: Implementação usando API TMDB
- `infrastructure/external/tmdb_client.py`: Cliente HTTP para TMDB
- `repositories/movie_repository.py`: Repositório concreto de filmes
- `repositories/memory_user_repository.py`: Repositório de usuários em memória
- `repositories/memory_blacklist_repository.py`: Repositório de blacklist JWT em memória

**Características**:
- Implementa interfaces definidas no domínio
- Adapta APIs externas ao formato esperado
- Pode ser substituída facilmente (MockDataSource para testes)
- Exemplo de Adapter Pattern

### 2.5 CAMADA DE CONFIGURAÇÃO (app/config.py)

**Responsabilidade**: Gerenciar variáveis de ambiente e configurações

**Variáveis**:
- `TMDB_API_KEY`: Chave da API do The Movie Database
- `SECRET_KEY`: Chave secreta para assinatura dos tokens JWT
- `APP_NAME`, `APP_VERSION`, `LOG_LEVEL`, `DEBUG`

**Características**:
- Usa Pydantic Settings
- Carrega de arquivo .env
- Centralizado em um único lugar
- Type-safe com validação


## 3. AUTENTICAÇÃO JWT

### 3.1 Fluxo Completo

```
POST /register → cria usuário, sem token

POST /login    → verifica senha
               → gera JWT (exp: 24h)
               → retorna token ao cliente

POST /logout   → recebe token
               → adiciona na blacklist
               → token não pode mais ser usado
```

### 3.2 Estrutura do Token JWT

```python
payload = {
    "sub": user.id,                              # ID do usuário
    "exp": (datetime.now() + timedelta(hours=24)).timestamp(),  # expiração
    "iat": datetime.now().timestamp()            # emitido em
}
```

### 3.3 Estratégia de Blacklist

O logoff é implementado via blacklist em memória:

- Apenas tokens **invalidados por logoff** são armazenados
- Cada token é salvo com sua data de expiração: `{token: exp}`
- Tokens expirados são removidos automaticamente via `clear_expired_tokens()`
- A blacklist nunca cresce infinitamente

```
Login  → gera token, não armazena nada no servidor
Uso    → verifica assinatura + verifica se NÃO está na blacklist
Logoff → adiciona token na blacklist com seu prazo de expiração
Limpeza→ tokens vencidos são removidos da blacklist automaticamente
```

### 3.4 Por que não armazenar todos os tokens gerados?

O JWT é **stateless** — o servidor não precisa guardar tokens válidos, pois a validade é verificada pela assinatura criptográfica. Guardar todos os tokens seria desnecessário e faria o armazenamento crescer sem controle.


## 4. PRINCÍPIOS APLICADOS

### 4.1 DEPENDENCY INJECTION (DI)

A aplicação usa injeção de dependências para desacoplar componentes:

```
Endpoint → instancia use case com repositório
Use Case → recebe repositório via __init__
Repositório → implementa interface do domínio
```

### 4.2 INVERSÃO DE DEPENDÊNCIA (DIP)

Módulos dependem de abstrações, não de implementações concretas:

```
✓ BOM:
  LogoutUser → IBlacklistRepository (interface)
               ↓
               MemoryBlacklistRepository (implementação)

✗ RUIM:
  LogoutUser → MemoryBlacklistRepository (acoplado)
```

### 4.3 SINGLE RESPONSIBILITY PRINCIPLE (SRP)

| Classe | Responsabilidade |
|--------|------------------|
| Movie / User | Encapsular dados e regras da entidade |
| token_service | Criar, verificar e invalidar tokens JWT |
| LoginUser | Autenticar usuário |
| LogoutUser | Invalidar token na blacklist |
| MemoryBlacklistRepository | Persistir tokens invalidados |

### 4.4 OPEN/CLOSED PRINCIPLE (OCP)

Aberto para extensão, fechado para modificação:

- Trocar blacklist em memória por Redis? → Implementar `IBlacklistRepository`
- Trocar TMDB por outro serviço? → Implementar `IMovieDataSource`
- Adicionar novo tipo de recomendação? → Estender `IDomainService`


## 5. FLUXO DE DADOS

### 5.1 Requisição de Login

```
1. POST /api/v1/users/login {"username": "...", "password": "..."}
   ↓
2. Endpoint user.login() valida body com Pydantic
   ↓
3. LoginUser.execute() verifica senha no repositório
   ↓
4. token_service.create_token(user) gera JWT
   ↓
5. Retorna UserResponse com token
```

### 5.2 Requisição de Logout

```
1. POST /api/v1/users/logout {"token": "eyJ..."}
   ↓
2. Endpoint user.logout() valida body com Pydantic
   ↓
3. LogoutUser.execute(token) chama blacklist_token()
   ↓
4. MemoryBlacklistRepository.add_token() decodifica e armazena
   ↓
5. Retorna UserLogoutResponse com mensagem de sucesso
```


## 6. ESTRUTURA DE DIRETÓRIOS

```
moodflix-main/
│
├── app/
│   ├── config.py                          # Configurações (TMDB_API_KEY, SECRET_KEY)
│   ├── main.py                            # Aplicação principal
│   │
│   ├── domain/                            # CAMADA DE DOMÍNIO
│   │   ├── entities/
│   │   │   ├── movie.py                   # Entidade Movie
│   │   │   └── user.py                    # Entidade User
│   │   ├── repositories/
│   │   │   ├── movie_repository_interface.py
│   │   │   ├── user_repository_interface.py
│   │   │   └── blacklist_repository_interface.py  ← novo
│   │   └── services/
│   │       ├── domain_service_interface.py
│   │       ├── mood_recommendation_service.py
│   │       └── token_service.py           ← novo
│   │
│   ├── application/                       # CAMADA DE APLICAÇÃO
│   │   └── use_cases/
│   │       ├── recommend_movies.py
│   │       ├── register_user.py
│   │       ├── login_user.py              ← atualizado (gera JWT)
│   │       ├── logout_user.py             ← novo
│   │       ├── add_moodmap.py
│   │       └── set_default_moodmap.py
│   │
│   ├── api/                               # CAMADA DE APRESENTAÇÃO
│   │   └── v1/endpoints/
│   │       ├── movies.py
│   │       └── user.py                    ← atualizado (endpoint /logout)
│   │
│   ├── schemas/
│   │   ├── movie_schema.py
│   │   └── user_schema.py                 ← atualizado (UserLogout, UserLogoutResponse)
│   │
│   ├── repositories/                      # Implementações concretas
│   │   ├── movie_repository.py
│   │   ├── memory_user_repository.py
│   │   └── memory_blacklist_repository.py ← novo
│   │
│   └── infrastructure/
│       └── external/
│           ├── tmdb_data_source.py
│           └── tmdb_client.py
│
├── requirements.txt
└── .env                                   # TMDB_API_KEY + SECRET_KEY
```


## 7. DEPENDÊNCIAS DO PROJETO

**Framework Web**: FastAPI

**Autenticação**: PyJWT
- Geração e verificação de tokens JWT
- Algoritmo HS256

**Configuração**: pydantic-settings

**Cliente HTTP**: requests

**Banco de Dados** (futuro): SQLAlchemy


## 8. PRÓXIMOS PASSOS

1. ~~Autenticação com JWT~~ ✅
2. **Middleware de proteção de rotas**: verificar token automaticamente nas rotas protegidas
3. **Refresh Token**: tokens de longa duração para manter sessão
4. **Banco de Dados**: implementar com SQLAlchemy
5. **Cache**: Redis (pode substituir MemoryBlacklistRepository)
6. **Testes**: suite completa com pytest
7. **CI/CD**: GitHub Actions
8. **Containerização**: Docker


## CONCLUSÃO

A arquitetura MoodFlix segue rigorosamente os princípios de Clean Architecture,
garantindo um código independente de detalhes técnicos, fácil de testar,
flexível para mudanças e pronto para crescer.

---
Documentação atualizada em: maio/2026
Arquitetura: Clean Architecture (Robert C. Martin)
Framework: FastAPI
Python: 3.8+
