from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.live_youtube import (
    LiveYouTubeCreate,
    LiveYouTubeUpdate,
    LiveYouTubeOut,
)
from ..crud.live_youtube import (
    create_live_youtube as crud_create_live_youtube,
    list_live_youtube as crud_list_live_youtube,
    get_live_youtube as crud_get_live_youtube,
    update_live_youtube as crud_update_live_youtube,
    delete_live_youtube as crud_delete_live_youtube,
)

router = APIRouter(prefix="/live-youtube", tags=["live-youtube"])


@router.post("/", response_model=LiveYouTubeOut, status_code=201)
def create_live_youtube(
    payload: LiveYouTubeCreate,
    db: Session = Depends(get_db),
):
    """
    Cria uma Live / YouTube Talk.
    """
    asset = crud_create_live_youtube(db, payload)
    return asset


@router.get("/", response_model=List[LiveYouTubeOut])
def list_live_youtube(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(
        None,
        description="big_talk | one_talk | little_talk",
    ),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    """
    Lista Lives / YouTube Talks com filtros.
    """
    return crud_list_live_youtube(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{asset_id}", response_model=LiveYouTubeOut)
def get_live_youtube(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Detalhe de uma Live / YouTube Talk.
    """
    asset = crud_get_live_youtube(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Live/YouTube Talk não encontrado",
        )
    return asset


@router.put("/{asset_id}", response_model=LiveYouTubeOut)
def update_live_youtube(
    asset_id: int,
    payload: LiveYouTubeUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza uma Live / YouTube Talk.
    """
    asset = crud_update_live_youtube(db, asset_id, payload)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Live/YouTube Talk não encontrado",
        )
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_live_youtube(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta uma Live / YouTube Talk.
    """
    success = crud_delete_live_youtube(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Live/YouTube Talk não encontrado",
        )
    return None
