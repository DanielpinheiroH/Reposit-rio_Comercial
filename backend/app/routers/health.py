from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health", summary="Healthcheck simples")
def health_check():
    return {"status": "ok"}
