from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_youtube_shorts(db: Session, data: schemas.YoutubeShortsCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.post_youtube_shorts
    payload["plataforma"] = models.PlataformaEnum.youtube_shorts
    return create_asset(db, payload)


def list_youtube_shorts(
    db: Session,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    return list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.post_youtube_shorts,
        plataforma=models.PlataformaEnum.youtube_shorts,
        skip=skip,
        limit=limit,
        search=search,
    )
