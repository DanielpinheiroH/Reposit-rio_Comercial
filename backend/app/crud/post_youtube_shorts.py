# backend/app/crud/post_youtube_shorts.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models, schemas
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_post_youtube_shorts(
    db: Session,
    data: schemas.PostYouTubeShortsCreate,
) -> models.Asset:
    """
    Cria um Asset do tipo post_youtube_shorts na plataforma youtube_shorts.
    """
    payload = data.model_dump()
    payload.update(
        {
            "tipo_asset": models.TipoAssetEnum.post_youtube_shorts,
            "plataforma": models.PlataformaEnum.youtube_shorts,
        }
    )

    # Força formato padrão "shorts" se não vier
    if not payload.get("formato"):
        payload["formato"] = "shorts"

    return create_asset(db, payload)


def list_posts_youtube_shorts(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """
    Lista posts de YouTube Shorts com filtros opcionais.
    """
    items = list_assets(
        db=db,
        tipo_asset=models.TipoAssetEnum.post_youtube_shorts,
        plataforma=models.PlataformaEnum.youtube_shorts,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


def get_post_youtube_shorts(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    """
    Busca um YouTube Shorts pelo ID.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_youtube_shorts:
        return None
    return asset


def update_post_youtube_shorts(
    db: Session,
    asset_id: int,
    data: schemas.PostYouTubeShortsUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um YouTube Shorts. Retorna None se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_youtube_shorts:
        return None

    payload = data.model_dump(exclude_unset=True)
    updated = update_asset(db, asset, payload)
    return updated


def delete_post_youtube_shorts(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um YouTube Shorts. Retorna False se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_youtube_shorts:
        return False

    delete_asset(db, asset_id)
    return True


# -------------------------------------------------------------------
# Aliases de compatibilidade com código legado
# (ex.: crud.__init__.py importando create_youtube_shorts, list_youtube_shorts)
# -------------------------------------------------------------------

create_youtube_shorts = create_post_youtube_shorts
list_youtube_shorts = list_posts_youtube_shorts
