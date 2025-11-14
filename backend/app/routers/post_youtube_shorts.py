from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.assets_base import create_asset, list_assets, get_asset, update_asset, delete_asset
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_youtube_shorts import (
    PostYouTubeShortsCreate, PostYouTubeShortsUpdate, PostYouTubeShortsOut
)

router = APIRouter(prefix="/posts-youtube-shorts", tags=["posts-youtube-shorts"])

@router.post("/", response_model=PostYouTubeShortsOut, status_code=201)
def create_post_youtube_shorts(payload: PostYouTubeShortsCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data.update({
        "tipo_asset": TipoAssetEnum.post_youtube_shorts,
        "plataforma": PlataformaEnum.youtube_shorts,
    })
    return create_asset(db, data)

@router.get("/", response_model=List[PostYouTubeShortsOut])
def list_posts_youtube_shorts(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(None, description='shorts'),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    return list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_youtube_shorts.value,
        plataforma=PlataformaEnum.youtube_shorts.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )

@router.get("/{asset_id}", response_model=PostYouTubeShortsOut)
def get_post_youtube_shorts(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_youtube_shorts:
        raise HTTPException(status_code=404, detail="YouTube Shorts não encontrado")
    return asset

@router.put("/{asset_id}", response_model=PostYouTubeShortsOut)
def update_post_youtube_shorts(asset_id: int, payload: PostYouTubeShortsUpdate, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_youtube_shorts:
        raise HTTPException(status_code=404, detail="YouTube Shorts não encontrado")
    return update_asset(db, asset, payload.model_dump(exclude_unset=True))

@router.delete("/{asset_id}", status_code=204)
def delete_post_youtube_shorts(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_youtube_shorts:
        raise HTTPException(status_code=404, detail="YouTube Shorts não encontrado")
    delete_asset(db, asset_id)
