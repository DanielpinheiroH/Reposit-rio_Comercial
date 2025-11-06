from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_tiktok_post(db: Session, data: schemas.TikTokPostCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.post_tiktok
    payload["plataforma"] = models.PlataformaEnum.tiktok
    return create_asset(db, payload)


def list_tiktok_posts(
    db: Session,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    return list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.post_tiktok,
        plataforma=models.PlataformaEnum.tiktok,
        skip=skip,
        limit=limit,
        search=search,
    )
