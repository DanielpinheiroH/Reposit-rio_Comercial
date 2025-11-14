from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..crud import assets_base as crud
from ..schemas.post_facebook import (
    PostFacebookCreate,
    PostFacebookUpdate,
    PostFacebookOut,
)

router = APIRouter(prefix="/posts/facebook", tags=["Posts - Facebook"])


@router.get("", response_model=List[PostFacebookOut])
def list_facebook_posts(
    search: Optional[str] = Query(None, description="Busca em título/descrição/campanha/cliente"),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    items = crud.list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.post_facebook,
        plataforma=models.PlataformaEnum.facebook,
        formato="feed",
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


@router.post("", response_model=PostFacebookOut, status_code=201)
def create_facebook_post(
    payload: PostFacebookCreate,
    db: Session = Depends(get_db),
):
    data = payload.model_dump()
    data.update(
        dict(
            tipo_asset=models.TipoAssetEnum.post_facebook,
            plataforma=models.PlataformaEnum.facebook,
            formato="feed",
        )
    )
    created = crud.create_asset(db, data)
    return created


@router.get("/{asset_id}", response_model=PostFacebookOut)
def get_facebook_post(asset_id: int, db: Session = Depends(get_db)):
    obj = crud.get_asset(db, asset_id)
    if not obj or obj.tipo_asset != models.TipoAssetEnum.post_facebook:
        raise HTTPException(status_code=404, detail="Post Facebook não encontrado")
    return obj


@router.put("/{asset_id}", response_model=PostFacebookOut)
def update_facebook_post(
    asset_id: int,
    payload: PostFacebookUpdate,
    db: Session = Depends(get_db),
):
    obj = crud.get_asset(db, asset_id)
    if not obj or obj.tipo_asset != models.TipoAssetEnum.post_facebook:
        raise HTTPException(status_code=404, detail="Post Facebook não encontrado")

    data = payload.model_dump(exclude_unset=True)
    # mantém fixos:
    data.update(dict(plataforma=models.PlataformaEnum.facebook, formato="feed"))

    updated = crud.update_asset(db, obj, data)
    return updated


@router.delete("/{asset_id}", status_code=204)
def delete_facebook_post(asset_id: int, db: Session = Depends(get_db)):
    obj = crud.get_asset(db, asset_id)
    if not obj or obj.tipo_asset != models.TipoAssetEnum.post_facebook:
        raise HTTPException(status_code=404, detail="Post Facebook não encontrado")
    crud.delete_asset(db, asset_id)
