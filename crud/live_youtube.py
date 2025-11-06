from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_live_youtube(db: Session, data: schemas.LiveYoutubeCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.live_youtube
    payload["plataforma"] = models.PlataformaEnum.youtube
    return create_asset(db, payload)


def list_live_youtube(
    db: Session,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    return list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.live_youtube,
        plataforma=models.PlataformaEnum.youtube,
        skip=skip,
        limit=limit,
        search=search,
    )
