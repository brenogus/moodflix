"""Aplicacao MoodFlix API - Ponto de entrada.

Configuracao e inicializacao da aplicacao FastAPI.
Define roteadores, middleware e configuracoes globais.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.api.v1.endpoints import movies

# Configurar logging da aplicacao
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Gerenciador de ciclo de vida
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia inicializacao e encerramento da aplicacao."""
    # Inicializacao
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} iniciada")
    logger.info(f"Documentacao disponivel em: /docs")
    logger.debug(f"DEBUG mode: {settings.DEBUG}")
    
    yield  # Aplicacao roda aqui
    
    # Encerramento
    logger.info(f"{settings.APP_NAME} encerrada")

# Criar aplicacao FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API de recomendacao de filmes baseada em mood e genero usando Clean Architecture",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Registrar roteadores
app.include_router(movies.router, prefix="/api/v1", tags=["movies"])


# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """Verifica o status de saude da API.
    
    Endpoint simples para verificar se a API esta funcionando.
    
    Returns:
        Dicionario com status da aplicacao
    """
    return {"status": "healthy", "app": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Iniciando servidor Uvicorn na porta 8000")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    )

