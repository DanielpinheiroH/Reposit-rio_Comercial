from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .database import Base, engine
from .routers import (
    health,
    conteudo_especial,
    live_youtube,
    social_testemunhal,
    post_instagram,
    post_tiktok,
    post_kwai,
    post_youtube_shorts,
    metrics,
    collections,
)

settings = get_settings()

# cria tabelas no sqlite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.API_DEBUG,
)

# CORS direto (sem depender de env) para o frontend Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(conteudo_especial.router, prefix=settings.API_V1_STR)
app.include_router(live_youtube.router, prefix=settings.API_V1_STR)
app.include_router(social_testemunhal.router, prefix=settings.API_V1_STR)
app.include_router(post_instagram.router, prefix=settings.API_V1_STR)
app.include_router(post_tiktok.router, prefix=settings.API_V1_STR)
app.include_router(post_kwai.router, prefix=settings.API_V1_STR)
app.include_router(post_youtube_shorts.router, prefix=settings.API_V1_STR)
app.include_router(metrics.router, prefix=settings.API_V1_STR)
app.include_router(collections.router, prefix=settings.API_V1_STR)
