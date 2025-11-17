# backend/app/crud/post_kwai.py

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


def create_post_kwai(
    db: Session,
    data: schemas.PostKwaiCreate,
) -> models.Asset:
    """
    Cria um Asset do tipo post_kwai na plataforma kwai.
    """
    payload = data.model_dump()
    payload.update(
        {
            "tipo_asset": models.TipoAssetEnum.post_kwai,
            "plataforma": models.PlataformaEnum.kwai,
        }
    )

    # se quiser forçar formato padrão:
    if not payload.get("formato"):
        payload["formato"] = "feed"

    return create_asset(db, payload)


def list_posts_kwai(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """
    Lista posts do Kwai com filtros opcionais.
    """
    items = list_assets(
        db=db,
        tipo_asset=models.TipoAssetEnum.post_kwai,
        plataforma=models.PlataformaEnum.kwai,
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
) -> Optional[models.Asset]:
    """
    Busca um post do Kwai pelo ID.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_kwai:
        return None
    return asset


def update_post_kwai(
    db: Session,
    asset_id: int,
    data: schemas.PostKwaiUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um post do Kwai. Retorna None se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_kwai:
        return None

    payload = data.model_dump(exclude_unset=True)
    updated = update_asset(db, asset, payload)
    return updated


def delete_post_kwai(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um post do Kwai. Retorna False se não existir ou tipo diferente.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != models.TipoAssetEnum.post_kwai:
        return False

    delete_asset(db, asset_id)
    return True


# -------------------------------------------------------------------
# Aliases de compatibilidade com código legado
# (ex.: crud.__init__.py importando create_kwai_post, list_kwai_posts)
# -------------------------------------------------------------------

create_kwai_post = create_post_kwai
list_kwai_posts = list_posts_kwai
