# backend/app/routers/health.py

from typing import Dict
from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    summary="Healthcheck simples",
)
def health_check() -> Dict[str, str]:
    """
    Endpoint básico de healthcheck da API.
    Pode ser usado por monitoramento / load balancer.
    """
    return {"status": "ok"}
