# backend/app/crud/youtube_talk.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.youtube_talk import (
    YouTubeTalkCreate,
    YouTubeTalkUpdate,
    YouTubeTalkOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_youtube_talk(
    db: Session,
    payload: YouTubeTalkCreate,
) -> models.Asset:
    """
    Cria um YouTube Talk:
    - tipo_asset = youtube_talk
    - plataforma = youtube
    """
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.youtube_talk,
            "plataforma": PlataformaEnum.youtube,
        }
    )
    asset = create_asset(db, data)
    return asset


def list_youtube_talks(
    db: Session,
    formato: Optional[str] = None,          # big_talk | one_talk | little_talk
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[YouTubeTalkOut]:
    """
    Lista YouTube Talks com filtros opcionais.
    """
    assets = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.youtube_talk.value,
        plataforma=PlataformaEnum.youtube.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return assets


def get_youtube_talk(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    """
    Busca um YouTube Talk garantindo o tipo correto.
    Retorna None se não for youtube_talk.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.youtube_talk:
        return None
    return asset


def update_youtube_talk(
    db: Session,
    asset_id: int,
    payload: YouTubeTalkUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um YouTube Talk.
    Não permite trocar tipo_asset/plataforma.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.youtube_talk:
        return None

    data = payload.model_dump(exclude_unset=True)
    # Blindagem extra
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    updated = update_asset(db, asset, data)
    return updated


def delete_youtube_talk(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um YouTube Talk.
    Retorna:
    - True se deletou
    - False se não encontrou / tipo errado.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.youtube_talk:
        return False

    delete_asset(db, asset_id)
    return True
