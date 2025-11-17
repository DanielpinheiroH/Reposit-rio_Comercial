from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.post_youtube_shorts import (
    PostYouTubeShortsCreate,
    PostYouTubeShortsUpdate,
    PostYouTubeShortsOut,
)
from ..crud.post_youtube_shorts import (
    create_post_youtube_shorts as crud_create_post_youtube_shorts,
    list_posts_youtube_shorts as crud_list_posts_youtube_shorts,
    get_post_youtube_shorts as crud_get_post_youtube_shorts,
    update_post_youtube_shorts as crud_update_post_youtube_shorts,
    delete_post_youtube_shorts as crud_delete_post_youtube_shorts,
)

router = APIRouter(prefix="/posts-youtube-shorts", tags=["posts-youtube-shorts"])


@router.post("/", response_model=PostYouTubeShortsOut, status_code=201)
def create_post_youtube_shorts(
    payload: PostYouTubeShortsCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um YouTube Shorts.
    O CRUD já fixa tipo_asset=post_youtube_shorts e plataforma=youtube_shorts.
    """
    asset = crud_create_post_youtube_shorts(db, payload)
    return asset


@router.get("/", response_model=List[PostYouTubeShortsOut])
def list_posts_youtube_shorts(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(
        None,
        description="shorts",
    ),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    """
    Lista YouTube Shorts com filtros opcionais.
    """
    items = crud_list_posts_youtube_shorts(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


@router.get("/{asset_id}", response_model=PostYouTubeShortsOut)
def get_post_youtube_shorts(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Detalhe de um YouTube Shorts.
    """
    asset = crud_get_post_youtube_shorts(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="YouTube Shorts não encontrado",
        )
    return asset


@router.put("/{asset_id}", response_model=PostYouTubeShortsOut)
def update_post_youtube_shorts(
    asset_id: int,
    payload: PostYouTubeShortsUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um YouTube Shorts.
    """
    asset = crud_update_post_youtube_shorts(db, asset_id, payload)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="YouTube Shorts não encontrado",
        )
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_post_youtube_shorts(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta um YouTube Shorts.
    """
    success = crud_delete_post_youtube_shorts(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="YouTube Shorts não encontrado",
        )
    return None
