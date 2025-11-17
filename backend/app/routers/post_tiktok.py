from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.post_tiktok import (
    PostTikTokCreate,
    PostTikTokUpdate,
    PostTikTokOut,
)
from ..crud.post_tiktok import (
    create_post_tiktok as crud_create_post_tiktok,
    list_posts_tiktok as crud_list_posts_tiktok,
    get_post_tiktok as crud_get_post_tiktok,
    update_post_tiktok as crud_update_post_tiktok,
    delete_post_tiktok as crud_delete_post_tiktok,
)

router = APIRouter(prefix="/posts-tiktok", tags=["posts-tiktok"])


@router.post("/", response_model=PostTikTokOut, status_code=201)
def create_post_tiktok(
    payload: PostTikTokCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um Post do TikTok.
    O CRUD já fixa tipo_asset=post_tiktok e plataforma=tiktok.
    """
    asset = crud_create_post_tiktok(db, payload)
    return asset


@router.get("/", response_model=List[PostTikTokOut])
def list_posts_tiktok(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(
        None,
        description="feed",
    ),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    """
    Lista posts do TikTok com filtros opcionais.
    """
    items = crud_list_posts_tiktok(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


@router.get("/{asset_id}", response_model=PostTikTokOut)
def get_post_tiktok(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Detalhe de um Post do TikTok.
    """
    asset = crud_get_post_tiktok(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Post do TikTok não encontrado",
        )
    return asset


@router.put("/{asset_id}", response_model=PostTikTokOut)
def update_post_tiktok(
    asset_id: int,
    payload: PostTikTokUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um Post do TikTok.
    """
    asset = crud_update_post_tiktok(db, asset_id, payload)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Post do TikTok não encontrado",
        )
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_post_tiktok(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta um Post do TikTok.
    """
    success = crud_delete_post_tiktok(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Post do TikTok não encontrado",
        )
    return None
