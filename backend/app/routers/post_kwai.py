from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.post_kwai import (
    PostKwaiCreate,
    PostKwaiUpdate,
    PostKwaiOut,
)
from ..crud.post_kwai import (
    create_post_kwai as crud_create_post_kwai,
    list_posts_kwai as crud_list_posts_kwai,
    get_post_kwai as crud_get_post_kwai,
    update_post_kwai as crud_update_post_kwai,
    delete_post_kwai as crud_delete_post_kwai,
)

router = APIRouter(prefix="/posts-kwai", tags=["posts-kwai"])


@router.post("", response_model=PostKwaiOut, status_code=201)
def create_post_kwai(
    payload: PostKwaiCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um Post do Kwai.
    O CRUD já fixa tipo_asset=post_kwai e plataforma=kwai.
    """
    asset = crud_create_post_kwai(db, payload)
    return asset


@router.get("", response_model=List[PostKwaiOut])
def list_posts_kwai(
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
    Lista posts do Kwai com filtros opcionais.
    """
    items = crud_list_posts_kwai(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


@router.get("/{asset_id}", response_model=PostKwaiOut)
def get_post_kwai(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Detalhe de um Post do Kwai.
    """
    asset = crud_get_post_kwai(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Post do Kwai não encontrado",
        )
    return asset


@router.put("/{asset_id}", response_model=PostKwaiOut)
def update_post_kwai(
    asset_id: int,
    payload: PostKwaiUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um Post do Kwai.
    """
    asset = crud_update_post_kwai(db, asset_id, payload)
    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Post do Kwai não encontrado",
        )
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_post_kwai(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta um Post do Kwai.
    """
    success = crud_delete_post_kwai(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Post do Kwai não encontrado",
        )
    return None
