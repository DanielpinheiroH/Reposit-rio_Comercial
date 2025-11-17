from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.post_facebook import (
    PostFacebookCreate,
    PostFacebookUpdate,
    PostFacebookOut,
)
from ..crud.post_facebook import (
    list_facebook_posts as crud_list_facebook_posts,
    create_facebook_post as crud_create_facebook_post,
    get_facebook_post as crud_get_facebook_post,
    update_facebook_post as crud_update_facebook_post,
    delete_facebook_post as crud_delete_facebook_post,
)

router = APIRouter(prefix="/posts/facebook", tags=["Posts - Facebook"])


@router.get("", response_model=List[PostFacebookOut])
def list_facebook_posts(
    search: Optional[str] = Query(
        None,
        description="Busca em título/descrição/campanha/cliente",
    ),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    items = crud_list_facebook_posts(
        db=db,
        search=search,
        campanha=campanha,
        cliente=cliente,
        skip=skip,
        limit=limit,
    )
    return items


@router.post("", response_model=PostFacebookOut, status_code=201)
def create_facebook_post(
    payload: PostFacebookCreate,
    db: Session = Depends(get_db),
):
    created = crud_create_facebook_post(db, payload)
    return created


@router.get("/{asset_id}", response_model=PostFacebookOut)
def get_facebook_post(
    asset_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_get_facebook_post(db, asset_id)
    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Post Facebook não encontrado",
        )
    return obj


@router.put("/{asset_id}", response_model=PostFacebookOut)
def update_facebook_post(
    asset_id: int,
    payload: PostFacebookUpdate,
    db: Session = Depends(get_db),
):
    updated = crud_update_facebook_post(db, asset_id, payload)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Post Facebook não encontrado",
        )
    return updated


@router.delete("/{asset_id}", status_code=204)
def delete_facebook_post(
    asset_id: int,
    db: Session = Depends(get_db),
):
    success = crud_delete_facebook_post(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Post Facebook não encontrado",
        )
    return None
