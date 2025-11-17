# backend/app/crud/post_youtube_shorts.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_youtube_shorts import (
    PostYouTubeShortsCreate,
    PostYouTubeShortsUpdate,
    PostYouTubeShortsOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_post_youtube_shorts(
    db: Session,
    payload: PostYouTubeShortsCreate,
) -> models.Asset:
    """
    Cria um asset do tipo YouTube Shorts:
    - tipo_asset = post_youtube_shorts
    - plataforma = youtube_shorts
    """
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.post_youtube_shorts,
            "plataforma": PlataformaEnum.youtube_shorts,
        }
    )
    return create_asset(db, data)


def list_posts_youtube_shorts(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[PostYouTubeShortsOut]:
    """
    Lista YouTube Shorts com filtros opcionais.
    YTShortsFormato atualmente = 'shorts'.
    """
    items = list_assets(
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
    return items


def get_post_youtube_shorts(
    db: Session,
    asset_id: int,
):
    """
    Busca um YouTube Shorts garantindo o tipo correto.
    Retorna None se não for post_youtube_shorts.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_youtube_shorts:
        return None
    return asset


def update_post_youtube_shorts(
    db: Session,
    asset_id: int,
    payload: PostYouTubeShortsUpdate,
):
    """
    Atualiza um YouTube Shorts.
    Não permite trocar tipo_asset/plataforma.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_youtube_shorts:
        return None

    data = payload.model_dump(exclude_unset=True)
    # Blindagem extra
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    updated = update_asset(db, asset, data)
    return updated


def delete_post_youtube_shorts(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um YouTube Shorts.
    Retorna:
    - True se deletou
    - False se não encontrou / tipo errado.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_youtube_shorts:
        return False

    delete_asset(db, asset_id)
    return True
