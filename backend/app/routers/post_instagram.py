from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.assets_base import create_asset, list_assets, get_asset, update_asset, delete_asset
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_instagram import (
    PostInstagramCreate,
    PostInstagramUpdate,
    PostInstagramOut,
)

router = APIRouter(prefix="/posts-instagram", tags=["posts-instagram"])


@router.post("/", response_model=PostInstagramOut, status_code=201)
def create_post_instagram(payload: PostInstagramCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.post_instagram,
            "plataforma": PlataformaEnum.instagram,
        }
    )
    return create_asset(db, data)


@router.get("/", response_model=List[PostInstagramOut])
def list_posts_instagram(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(None, description='fixado_feed | feed | stories | reels'),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    assets = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_instagram.value,
        plataforma=PlataformaEnum.instagram.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return assets


@router.get("/{asset_id}", response_model=PostInstagramOut)
def get_post_instagram(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_instagram:
        raise HTTPException(status_code=404, detail="Post do Instagram não encontrado")
    return asset


@router.put("/{asset_id}", response_model=PostInstagramOut)
def update_post_instagram(asset_id: int, payload: PostInstagramUpdate, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_instagram:
        raise HTTPException(status_code=404, detail="Post do Instagram não encontrado")
    return update_asset(db, asset, payload.model_dump(exclude_unset=True))


@router.delete("/{asset_id}", status_code=204)
def delete_post_instagram(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_instagram:
        raise HTTPException(status_code=404, detail="Post do Instagram não encontrado")
    delete_asset(db, asset_id)
