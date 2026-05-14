"""Configurações centralizadas da aplicação.

Módulo responsável por gerenciar todas as variáveis de ambiente
e configurações da aplicação MoodFlix.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações de ambiente da aplicação MoodFlix.
    
    Carrega variáveis de ambiente do arquivo .env e valida tipos.
    Segue o padrão Singleton através de instância global 'settings'.
    
    Attributes:
        TMDB_API_KEY: Chave de API do The Movie Database (TMDB)
        APP_NAME: Nome da aplicação (padrão: 'MoodFlix API')
        APP_VERSION: Versão da aplicação (padrão: '1.0.0')
        LOG_LEVEL: Nível de logging (padrão: 'INFO')
    """
    
    TMDB_API_KEY: str
    SECRET_KEY : str
    APP_NAME: str = "MoodFlix API"
    APP_VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    class Config:
        """Configuração do Pydantic Settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instância global de configurações (Singleton)
settings: Settings = Settings()