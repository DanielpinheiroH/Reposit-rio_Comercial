# backend/app/crud/post_tiktok.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_tiktok import (
    PostTikTokCreate,
    PostTikTokUpdate,
    PostTikTokOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_post_tiktok(
    db: Session,
    payload: PostTikTokCreate,
) -> models.Asset:
    """
    Cria um asset do tipo Post TikTok:
    - tipo_asset = post_tiktok
    - plataforma = tiktok
    """
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.post_tiktok,
            "plataforma": PlataformaEnum.tiktok,
        }
    )
    return create_asset(db, data)


def list_posts_tiktok(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[PostTikTokOut]:
    """
    Lista posts do TikTok com filtros opcionais.
    TikTokFormato atualmente = 'feed'.
    """
    items = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_tiktok.value,
        plataforma=PlataformaEnum.tiktok.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


def get_post_tiktok(
    db: Session,
    asset_id: int,
):
    """
    Busca um Post TikTok garantindo o tipo correto.
    Retorna None se não for post_tiktok.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_tiktok:
        return None
    return asset


def update_post_tiktok(
    db: Session,
    asset_id: int,
    payload: PostTikTokUpdate,
):
    """
    Atualiza um Post TikTok.
    Não permite trocar tipo_asset/plataforma.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_tiktok:
        return None

    data = payload.model_dump(exclude_unset=True)
    # Blindagem extra
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    updated = update_asset(db, asset, data)
    return updated


def delete_post_tiktok(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um Post TikTok.
    Retorna:
    - True se deletou
    - False se não encontrou / tipo errado.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_tiktok:
        return False

    delete_asset(db, asset_id)
    return True
