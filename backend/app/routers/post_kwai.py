from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.assets_base import create_asset, list_assets, get_asset, update_asset, delete_asset
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_kwai import (
    PostKwaiCreate, PostKwaiUpdate, PostKwaiOut
)

router = APIRouter(prefix="/posts-kwai", tags=["posts-kwai"])

@router.post("/", response_model=PostKwaiOut, status_code=201)
def create_post_kwai(payload: PostKwaiCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data.update({
        "tipo_asset": TipoAssetEnum.post_kwai,
        "plataforma": PlataformaEnum.kwai,
    })
    return create_asset(db, data)

@router.get("/", response_model=List[PostKwaiOut])
def list_posts_kwai(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(None, description='feed'),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    return list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_kwai.value,
        plataforma=PlataformaEnum.kwai.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )

@router.get("/{asset_id}", response_model=PostKwaiOut)
def get_post_kwai(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_kwai:
        raise HTTPException(status_code=404, detail="Post do Kwai não encontrado")
    return asset

@router.put("/{asset_id}", response_model=PostKwaiOut)
def update_post_kwai(asset_id: int, payload: PostKwaiUpdate, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_kwai:
        raise HTTPException(status_code=404, detail="Post do Kwai não encontrado")
    return update_asset(db, asset, payload.model_dump(exclude_unset=True))

@router.delete("/{asset_id}", status_code=204)
def delete_post_kwai(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_kwai:
        raise HTTPException(status_code=404, detail="Post do Kwai não encontrado")
    delete_asset(db, asset_id)
