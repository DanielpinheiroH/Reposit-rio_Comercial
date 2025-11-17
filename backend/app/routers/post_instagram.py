from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.post_instagram import (
    create_post_instagram as crud_create_post_instagram,
    list_posts_instagram as crud_list_posts_instagram,
    get_post_instagram as crud_get_post_instagram,
    update_post_instagram as crud_update_post_instagram,
    delete_post_instagram as crud_delete_post_instagram,
)
from ..schemas.post_instagram import (
    PostInstagramCreate,
    PostInstagramUpdate,
    PostInstagramOut,
)

router = APIRouter(prefix="/posts-instagram", tags=["posts-instagram"])


@router.post("/", response_model=PostInstagramOut, status_code=201)
def create_post_instagram(
    payload: PostInstagramCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um Post do Instagram.
    O CRUD já fixa tipo_asset=post_instagram e plataforma=instagram.
    """
    asset = crud_create_post_instagram(db, payload)
    return asset


@router.get("/", response_model=List[PostInstagramOut])
def list_posts_instagram(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(
        None,
        description="fixado_feed | feed | stories | reels",
    ),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    """
    Lista posts do Instagram com filtros opcionais.
    """
    assets = crud_list_posts_instagram(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return assets


@router.get("/{asset_id}", response_model=PostInstagramOut)
def get_post_instagram(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Busca um Post do Instagram pelo ID.
    """
    asset = crud_get_post_instagram(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Post do Instagram não encontrado",
        )
    return asset


@router.put("/{asset_id}", response_model=PostInstagramOut)
def update_post_instagram(
    asset_id: int,
    payload: PostInstagramUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um Post do Instagram.
    """
    asset = crud_update_post_instagram(db, asset_id, payload)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Post do Instagram não encontrado",
        )
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_post_instagram(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta um Post do Instagram.
    """
    success = crud_delete_post_instagram(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Post do Instagram não encontrado",
        )
    # 204 No Content → não retorna body
    return None
