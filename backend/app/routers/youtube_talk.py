from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.assets_base import create_asset, list_assets, get_asset, update_asset, delete_asset
from ..models import TipoAssetEnum, PlataformaEnum, Asset
from ..schemas.youtube_talk import (
    YouTubeTalkCreate,
    YouTubeTalkUpdate,
    YouTubeTalkOut,
)

router = APIRouter(prefix="/youtube-talks", tags=["youtube-talks"])


@router.post("/", response_model=YouTubeTalkOut, status_code=201)
def create_youtube_talk(payload: YouTubeTalkCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.youtube_talk,
            "plataforma": PlataformaEnum.youtube,
        }
    )
    asset = create_asset(db, data)
    return asset


@router.get("/", response_model=List[YouTubeTalkOut])
def list_youtube_talks(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(None, description='big_talk | one_talk | little_talk'),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    assets = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.youtube_talk.value,
        plataforma=PlataformaEnum.youtube.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return assets


@router.get("/{asset_id}", response_model=YouTubeTalkOut)
def get_youtube_talk_by_id(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.youtube_talk:
        raise HTTPException(status_code=404, detail="YouTube Talk não encontrado")
    return asset


@router.put("/{asset_id}", response_model=YouTubeTalkOut)
def update_youtube_talk_by_id(asset_id: int, payload: YouTubeTalkUpdate, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.youtube_talk:
        raise HTTPException(status_code=404, detail="YouTube Talk não encontrado")

    updated = update_asset(db, asset, payload.model_dump(exclude_unset=True))
    return updated


@router.delete("/{asset_id}", status_code=204)
def delete_youtube_talk_by_id(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.youtube_talk:
        raise HTTPException(status_code=404, detail="YouTube Talk não encontrado")
    delete_asset(db, asset_id)
