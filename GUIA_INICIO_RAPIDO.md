"""
GUIA DE INICIO RAPIDO - MOODFLIX API
=====================================

## 1. INSTALACAO (5 minutos)

### Passo 1: Clonar/Acessar o projeto
cd c:\Users\breno\OneDrive\Documentos\moodflix-main

### Passo 2: Criar ambiente virtual
python -m venv venv

### Passo 3: Ativar ambiente (Windows)
venv\Scripts\activate

### Passo 4: Instalar dependencias
pip install -r requirements.txt

### Passo 5: Criar arquivo .env
Copiar .env.example para .env e adicionar sua chave TMDB_API_KEY
(Obter em: https://www.themoviedb.org/settings/api)


## 2. EXECUTAR A APLICACAO

### Opcao 1: Via Python direto
python app/main.py

### Opcao 2: Via Uvicorn
uvicorn app.main:app --reload --port 8000

### Resultado esperado:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     MoodFlix API iniciada
INFO:     Documentacao disponivel em: /docs
```


## 3. ACESSAR A APLICACAO

- API: http://localhost:8000
- Documentacao Swagger: http://localhost:8000/docs
- Documentacao ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health


## 4. TESTAR ENDPOINTS

### 4.1 Health Check
curl http://localhost:8000/health

Response:
{
  "status": "healthy",
  "app": "MoodFlix API"
}

### 4.2 Recomendacoes por Genero
curl "http://localhost:8000/api/v1/recommend?genre=acao"

### 4.3 Recomendacoes por Mood
curl "http://localhost:8000/api/v1/recommend?mood=feliz"

### 4.4 Listar Filmes (em desenvolvimento)
curl "http://localhost:8000/api/v1/movies?limit=10"


## 5. ESTRUTURA DO PROJETO

moodflix-main/
├── ARQUITETURA.md          ← Leia isto para entender o design
├── README.md               ← Documentacao principal
├── .env.example            ← Modelo de configuracoes
├── requirements.txt        ← Dependencias Python
│
└── app/
    ├── config.py           ← Configuracoes de ambiente
    ├── main.py             ← Aplicacao FastAPI
    │
    ├── domain/             ← Logica de negocio pura
    │   ├── entities/       ← Modelos de negocio
    │   ├── repositories/   ← Interfaces
    │   └── services/       ← Servicos de dominio
    │
    ├── aplication/         ← Casos de uso
    │   └── use_cases/      
    │
    ├── api/                ← Endpoints HTTP
    │   └── v1/endpoints/   
    │
    ├── infrastructure/     ← Detalhes tecnicos
    │   ├── external/       ← APIs externas
    │   └── db/             ← Banco de dados
    │
    ├── schemas/            ← DTOs Pydantic
    └── utils/              ← Funcoes auxiliares


## 6. GENEROS SUPORTADOS

- acao
- comedia
- drama
- ficcao
- romance
- animacao
- terror


## 7. MOODS SUPORTADOS

- triste
- feliz
- pensativo
- romantico


## 8. ARQUIVOS IMPORTANTES PARA ENTENDER O PROJETO

1. **ARQUITETURA.md** - Leia PRIMEIRO
   Explica a arquitetura completa do projeto
   Mostra como cada camada funciona
   Explica os padroes de design utilizados

2. **README.md** - Leia para detalhes
   Como instalar e executar
   API endpoints documentados
   Dependencias do projeto

3. **Docstrings no codigo** - Leia conforme necessario
   Cada classe tem documentacao completa
   Cada metodo tem exemplos de uso
   Type hints em todos os parametros


## 9. PRINCIPIOS IMPORTANTES

### Dependency Injection
O projeto usa injecao de dependencias:
- Use cases recebem repositorio como parametro
- Repository recebe data source como parametro
- Facilita testes unitarios

### Clean Architecture
4 camadas bem definidas:
1. Domain (entidades e logica de negocio)
2. Application (use cases)
3. Presentation (endpoints HTTP)
4. Infrastructure (detalhes tecnicos)

### SOLID Principles
- Single Responsibility: Cada classe tem uma responsabilidade
- Open/Closed: Aberto para extensao
- Liskov Substitution: Pode substituir implementacoes
- Interface Segregation: Interfaces pequenas
- Dependency Inversion: Depende de abstracos


## 10. COMO ADICIONAR UMA NOVA FUNCIONALIDADE

### Exemplo: Novo tipo de recomendacao

1. Criar nova interface em domain/services/
2. Implementar servico em domain/services/
3. Criar novo use case em aplication/use_cases/
4. Criar novo endpoint em api/v1/endpoints/
5. Testar via Swagger (/docs)


## 11. CONFIGURACOES IMPORTANTES

Arquivo .env:
```
TMDB_API_KEY=sua_chave_aqui
APP_NAME=MoodFlix API
APP_VERSION=1.0.0
LOG_LEVEL=INFO
DEBUG=False
```


## 12. PROBLEMAS COMUNS

### Erro: "No module named 'app'"
Solucao: Garantir que esta na pasta raiz do projeto
Executar: cd moodflix-main

### Erro: "TMDB_API_KEY not found"
Solucao: Criar arquivo .env com TMDB_API_KEY
Referencia: Copiar de .env.example

### Erro: "Connection refused"
Solucao: Garantir que a aplicacao esta rodando
Executar: python app/main.py


## 13. DICAS DE DESENVOLVIMENTO

1. Use a documentacao Swagger (/docs) para testar endpoints
2. Veja os logs da aplicacao para debug
3. Crie testes para suas funcionalidades
4. Siga a estrutura de arquivos existente
5. Mantenha as responsabilidades separadas


## 14. PROXIMOS PASSOS

1. Instalar dependencias
2. Configurar .env
3. Executar aplicacao
4. Acessar http://localhost:8000/docs
5. Testar endpoints
6. Ler ARQUITETURA.md para entender o design
7. Explorar o codigo com docstrings


## 15. RECURSOS UTEIS

- FastAPI docs: https://fastapi.tiangolo.com/
- Pydantic docs: https://docs.pydantic.dev/
- TMDB API: https://www.themoviedb.org/settings/api
- Clean Architecture: Robert C. Martin
- SOLID Principles: Wikipedia


## SUPORTE

Para duvidas sobre arquitetura: Consulte ARQUITETURA.md
Para duvidas sobre uso: Consulte README.md
Para duvidas sobre codigo: Veja docstrings no arquivo
Para duvidas sobre dependencias: Consulte requirements.txt


---
"""
