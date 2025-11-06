from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_social_testemunhal(db: Session, data: schemas.SocialTestemunhalCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.social_video_testemunhal
    return create_asset(db, payload)


def list_social_testemunhal(
    db: Session,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    return list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.social_video_testemunhal,
        skip=skip,
        limit=limit,
        search=search,
    )
