# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .database import Base, engine
from .routers import (
    health,
    conteudo_especial,
    live_youtube,          # Lives/Talks YouTube (big_talk | one_talk | little_talk via formato)
    social_testemunhal,
    post_instagram,
    post_tiktok,
    post_kwai,
    post_youtube_shorts,
    post_facebook,        # Facebook Feed
    youtube_talk,         # <- NOVO: router específico de YouTube Talks, se quiser usar
    metrics,
    collections,
)

settings = get_settings()

# cria tabelas no sqlite (ambiente de dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.API_DEBUG,
)

# CORS para o frontend Vite
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
app.include_router(live_youtube.router, prefix=settings.API_V1_STR)          # YouTube Lives / Talks
app.include_router(social_testemunhal.router, prefix=settings.API_V1_STR)
app.include_router(post_instagram.router, prefix=settings.API_V1_STR)
app.include_router(post_tiktok.router, prefix=settings.API_V1_STR)
app.include_router(post_kwai.router, prefix=settings.API_V1_STR)
app.include_router(post_youtube_shorts.router, prefix=settings.API_V1_STR)
app.include_router(post_facebook.router, prefix=settings.API_V1_STR)         # Facebook Feed
app.include_router(youtube_talk.router, prefix=settings.API_V1_STR)          # YouTube Talks (schema próprio)
app.include_router(metrics.router, prefix=settings.API_V1_STR)
app.include_router(collections.router, prefix=settings.API_V1_STR)
