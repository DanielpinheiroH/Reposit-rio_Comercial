# backend/app/crud/post_instagram.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_instagram import (
    PostInstagramCreate,
    PostInstagramUpdate,
    PostInstagramOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_post_instagram(
    db: Session,
    payload: PostInstagramCreate,
) -> models.Asset:
    """
    Cria um asset do tipo Post Instagram, fixando:
    - tipo_asset = post_instagram
    - plataforma = instagram
    """
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.post_instagram,
            "plataforma": PlataformaEnum.instagram,
        }
    )
    return create_asset(db, data)


def list_posts_instagram(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[PostInstagramOut]:
    """
    Lista posts de Instagram com filtros opcionais.
    """
    assets = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_instagram.value,
        plataforma=PlataformaEnum.instagram.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return assets  # será convertido para PostInstagramOut pelo response_model


def get_post_instagram(
    db: Session,
    asset_id: int,
):
    """
    Busca um Post Instagram garantindo o tipo correto.
    Retorna None se não for do tipo post_instagram.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_instagram:
        return None
    return asset


def update_post_instagram(
    db: Session,
    asset_id: int,
    payload: PostInstagramUpdate,
):
    """
    Atualiza um Post Instagram.
    Não permite trocar tipo_asset/plataforma.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_instagram:
        return None

    data = payload.model_dump(exclude_unset=True)
    # Blindagem, caso alguém tente mandar isso no body:
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    updated = update_asset(db, asset, data)
    return updated


def delete_post_instagram(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um Post Instagram.
    Retorna:
    - True se deletou
    - False se não encontrou / tipo errado
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_instagram:
        return False

    delete_asset(db, asset_id)
    return True
