# backend/app/crud/post_kwai.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_kwai import (
    PostKwaiCreate,
    PostKwaiUpdate,
    PostKwaiOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_post_kwai(
    db: Session,
    payload: PostKwaiCreate,
) -> models.Asset:
    """
    Cria um asset do tipo Post Kwai:
    - tipo_asset = post_kwai
    - plataforma = kwai
    - formato geralmente = 'feed' (controlado no schema/camada de chamada)
    """
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.post_kwai,
            "plataforma": PlataformaEnum.kwai,
        }
    )
    return create_asset(db, data)


def list_posts_kwai(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[PostKwaiOut]:
    """
    Lista posts do Kwai com filtros opcionais.
    KwaiFormato atualmente = 'feed'.
    """
    items = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_kwai.value,
        plataforma=PlataformaEnum.kwai.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


def get_post_kwai(
    db: Session,
    asset_id: int,
):
    """
    Busca um Post Kwai garantindo o tipo correto.
    Retorna None se não for post_kwai.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_kwai:
        return None
    return asset


def update_post_kwai(
    db: Session,
    asset_id: int,
    payload: PostKwaiUpdate,
):
    """
    Atualiza um Post Kwai.
    Não permite trocar tipo_asset/plataforma.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_kwai:
        return None

    data = payload.model_dump(exclude_unset=True)
    # Blindagem extra
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    updated = update_asset(db, asset, data)
    return updated


def delete_post_kwai(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um Post Kwai.
    Retorna:
    - True se deletou
    - False se não encontrou / tipo errado.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.post_kwai:
        return False

    delete_asset(db, asset_id)
    return True
