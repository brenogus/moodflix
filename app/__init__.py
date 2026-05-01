"""
MoodFlix API - Sistema de Recomendação de Filmes

Uma API REST que recomenda filmes baseado em genero ou estado emocional (mood)
do usuário, implementada com Clean Architecture.

Modulos principais:
- app.domain: Lógica de negócio pura (entidades, interfaces)
- app.aplication: Casos de uso (orquestração da lógica)
- app.api: Endpoints HTTP (camada de apresentação)
- app.infrastructure: Detalhes técnicos (TMDB, banco, etc)

Para iniciar:
    python app/main.py

Para documentacao interativa:
    http://localhost:8000/docs
    http://localhost:8000/redoc

Para mais informacoes:
    Consulte ARQUITETURA.md
"""

__version__ = "1.0.0"
__author__ = "Breno Gustavo de Oliveira e Ferreira"
