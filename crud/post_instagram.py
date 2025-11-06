from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_instagram_post(db: Session, data: schemas.InstagramPostCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.post_instagram
    payload["plataforma"] = models.PlataformaEnum.instagram
    return create_asset(db, payload)


def list_instagram_posts(
    db: Session,
    formato: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    items = list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.post_instagram,
        plataforma=models.PlataformaEnum.instagram,
        skip=skip,
        limit=limit,
        search=search,
    )
    if formato:
        items = [a for a in items if a.formato == formato]
    return items
