from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_kwai_post(db: Session, data: schemas.KwaiPostCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.post_kwai
    payload["plataforma"] = models.PlataformaEnum.kwai
    return create_asset(db, payload)


def list_kwai_posts(
    db: Session,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    return list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.post_kwai,
        plataforma=models.PlataformaEnum.kwai,
        skip=skip,
       limit=limit,
        search=search,
    )
