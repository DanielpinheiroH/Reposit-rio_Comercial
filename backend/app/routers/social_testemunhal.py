from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..crud.social_testemunhal import (
    create_social_testemunhal,
    get_social_testemunhal,
    update_social_testemunhal,
    delete_social_testemunhal,
    list_social_testemunhal,
)
from ..schemas.social_testemunhal import (
    SocialTestemunhalCreate,
    SocialTestemunhalUpdate,
    SocialTestemunhalOut,
)

router = APIRouter(prefix="/social-testemunhal", tags=["Social Vídeo Testemunhal"])


@router.get("/", response_model=List[SocialTestemunhalOut])
def api_list_social_testemunhal(
    plataforma: Optional[str] = Query(
        default=None,
        description="Filtra por plataforma ('instagram' ou 'tiktok').",
    ),
    duracao_seg: Optional[int] = Query(
        default=None,
        description="Filtra duração: 30 ou 60 (segundos).",
    ),
    search: Optional[str] = Query(default=None, description="Busca texto livre."),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    if plataforma and plataforma not in ("instagram", "tiktok"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Plataforma inválida. Use 'instagram' ou 'tiktok'.",
        )
    if duracao_seg and duracao_seg not in (30, 60):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="duracao_seg deve ser 30 ou 60.",
        )

    return list_social_testemunhal(
        db,
        plataforma=plataforma,
        duracao_seg=duracao_seg,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/",
    response_model=SocialTestemunhalOut,
    status_code=status.HTTP_201_CREATED,
)
def api_create_social_testemunhal(
    payload: SocialTestemunhalCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_social_testemunhal(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("/{asset_id}", response_model=SocialTestemunhalOut)
def api_get_social_testemunhal(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = get_social_testemunhal(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.social_video_testemunhal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testemunhal não encontrado.",
        )
    return asset


@router.put("/{asset_id}", response_model=SocialTestemunhalOut)
def api_update_social_testemunhal(
    asset_id: int,
    payload: SocialTestemunhalUpdate,
    db: Session = Depends(get_db),
):
    # Validações extras antes de ir pro CRUD
    if payload.plataforma and payload.plataforma not in ("instagram", "tiktok"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Plataforma inválida.",
        )
    if payload.formato and payload.formato != "reels":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato deve ser 'reels'.",
        )

    try:
        asset = update_social_testemunhal(db, asset_id, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testemunhal não encontrado.",
        )

    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_social_testemunhal(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = get_social_testemunhal(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.social_video_testemunhal:
        # Idempotente: 204 mesmo se já não existe ou não é do tipo
        return
    delete_social_testemunhal(db, asset_id)
    return
