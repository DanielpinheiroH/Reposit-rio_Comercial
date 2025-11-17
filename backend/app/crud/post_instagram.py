# backend/app/crud/post_instagram.py

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


def create_post_instagram(
    db: Session,
    data: schemas.PostInstagramCreate,
) -> models.Asset:
    """
    Cria um Asset do tipo post_instagram na plataforma instagram.
    """
    payload = data.model_dump()
    payload.update(
        {
            "tipo_asset": models.TipoAssetEnum.post_instagram,
            "plataforma": models.PlataformaEnum.instagram,
        }
    )
    return create_asset(db, payload)


def list_posts_instagram(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """
    Lista posts de Instagram com filtros opcionais.
    """
    items = list_assets(
        db=db,
        tipo_asset=models.TipoAssetEnum.post_instagram,
        plataforma=models.PlataformaEnum.instagram,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


def get_post_instagram(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    """
    Busca um post do Instagram pelo ID, garantindo que o tipo seja post_instagram.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_instagram:
        return None
    return asset


def update_post_instagram(
    db: Session,
    asset_id: int,
    data: schemas.PostInstagramUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um post do Instagram. Retorna None se não existir ou não for do tipo correto.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_instagram:
        return None

    payload = data.model_dump(exclude_unset=True)
    updated = update_asset(db, asset, payload)
    return updated


def delete_post_instagram(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um post do Instagram. Retorna False se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_instagram:
        return False

    delete_asset(db, asset_id)
    return True


# -------------------------------------------------------------------
# Aliases de compatibilidade com código legado
# (ex.: crud.__init__.py ainda importando create_instagram_post, etc.)
# -------------------------------------------------------------------

# Assinaturas antigas:
#   create_instagram_post(db, data)
#   list_instagram_posts(db, formato=None, search=None, skip=0, limit=50)

create_instagram_post = create_post_instagram
list_instagram_posts = list_posts_instagram
