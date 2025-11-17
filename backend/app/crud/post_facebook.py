# backend/app/crud/post_facebook.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.post_facebook import (
    PostFacebookCreate,
    PostFacebookUpdate,
    PostFacebookOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def list_facebook_posts(
    db: Session,
    search: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[PostFacebookOut]:
    """
    Lista posts de Facebook:
    - tipo_asset = post_facebook
    - plataforma = facebook
    - formato = feed
    """
    items = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.post_facebook,
        plataforma=PlataformaEnum.facebook,
        formato="feed",
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


def create_facebook_post(
    db: Session,
    payload: PostFacebookCreate,
) -> models.Asset:
    """
    Cria um post de Facebook com campos fixos:
    - tipo_asset = post_facebook
    - plataforma = facebook
    - formato = feed
    """
    data = payload.model_dump()
    data.update(
        dict(
            tipo_asset=TipoAssetEnum.post_facebook,
            plataforma=PlataformaEnum.facebook,
            formato="feed",
        )
    )
    created = create_asset(db, data)
    return created


def get_facebook_post(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    """
    Busca um post de Facebook, garantindo o tipo correto.
    """
    obj = get_asset(db, asset_id)
    if not obj or obj.tipo_asset != TipoAssetEnum.post_facebook:
        return None
    return obj


def update_facebook_post(
    db: Session,
    asset_id: int,
    payload: PostFacebookUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um post de Facebook.
    Mantém:
    - plataforma = facebook
    - formato = feed
    """
    obj = get_asset(db, asset_id)
    if not obj or obj.tipo_asset != TipoAssetEnum.post_facebook:
        return None

    data = payload.model_dump(exclude_unset=True)

    # mantém fixos:
    data.update(
        dict(
            plataforma=PlataformaEnum.facebook,
            formato="feed",
        )
    )

    updated = update_asset(db, obj, data)
    return updated


def delete_facebook_post(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um post de Facebook.
    Retorna:
    - True se deletou
    - False se não encontrou ou não era do tipo correto
    """
    obj = get_asset(db, asset_id)
    if not obj or obj.tipo_asset != TipoAssetEnum.post_facebook:
        return False

    delete_asset(db, asset_id)
    return True
