# backend/app/crud/post_tiktok.py

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


def create_post_tiktok(
    db: Session,
    data: schemas.PostTikTokCreate,
) -> models.Asset:
    """
    Cria um Asset do tipo post_tiktok na plataforma tiktok.
    """
    payload = data.model_dump()
    payload.update(
        {
            "tipo_asset": models.TipoAssetEnum.post_tiktok,
            "plataforma": models.PlataformaEnum.tiktok,
        }
    )
    # se quiser forçar formato padrão:
    if not payload.get("formato"):
        payload["formato"] = "feed"

    return create_asset(db, payload)


def list_posts_tiktok(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """
    Lista posts de TikTok com filtros opcionais.
    """
    items = list_assets(
        db=db,
        tipo_asset=models.TipoAssetEnum.post_tiktok,
        plataforma=models.PlataformaEnum.tiktok,
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
) -> Optional[models.Asset]:
    """
    Busca um post do TikTok pelo ID.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_tiktok:
        return None
    return asset


def update_post_tiktok(
    db: Session,
    asset_id: int,
    data: schemas.PostTikTokUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um post do TikTok. Retorna None se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_tiktok:
        return None

    payload = data.model_dump(exclude_unset=True)
    updated = update_asset(db, asset, payload)
    return updated


def delete_post_tiktok(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um post do TikTok. Retorna False se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_tiktok:
        return False

    delete_asset(db, asset_id)
    return True


# -------------------------------------------------------------------
# Aliases de compatibilidade com código legado
# (ex.: crud.__init__.py importando create_tiktok_post, list_tiktok_posts)
# -------------------------------------------------------------------

create_tiktok_post = create_post_tiktok
list_tiktok_posts = list_posts_tiktok
