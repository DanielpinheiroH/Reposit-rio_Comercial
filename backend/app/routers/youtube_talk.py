from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.youtube_talk import (
    YouTubeTalkCreate,
    YouTubeTalkUpdate,
    YouTubeTalkOut,
)
from ..crud.youtube_talk import (
    create_youtube_talk as crud_create_youtube_talk,
    list_youtube_talks as crud_list_youtube_talks,
    get_youtube_talk as crud_get_youtube_talk,
    update_youtube_talk as crud_update_youtube_talk,
    delete_youtube_talk as crud_delete_youtube_talk,
)

router = APIRouter(prefix="/youtube-talks", tags=["youtube-talks"])


@router.post("/", response_model=YouTubeTalkOut, status_code=201)
def create_youtube_talk(
    payload: YouTubeTalkCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um YouTube Talk.
    O CRUD já fixa tipo_asset=youtube_talk e plataforma=youtube.
    """
    asset = crud_create_youtube_talk(db, payload)
    return asset


@router.get("/", response_model=List[YouTubeTalkOut])
def list_youtube_talks(
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
    Lista YouTube Talks com filtros opcionais.
    """
    assets = crud_list_youtube_talks(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return assets


@router.get("/{asset_id}", response_model=YouTubeTalkOut)
def get_youtube_talk_by_id(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Busca um YouTube Talk pelo ID.
    """
    asset = crud_get_youtube_talk(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="YouTube Talk não encontrado",
        )
    return asset


@router.put("/{asset_id}", response_model=YouTubeTalkOut)
def update_youtube_talk_by_id(
    asset_id: int,
    payload: YouTubeTalkUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um YouTube Talk.
    """
    asset = crud_update_youtube_talk(db, asset_id, payload)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="YouTube Talk não encontrado",
        )
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_youtube_talk_by_id(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta um YouTube Talk.
    """
    success = crud_delete_youtube_talk(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="YouTube Talk não encontrado",
        )
    return None
