# backend/app/crud/live_youtube.py

from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.live_youtube import (
    LiveYouTubeCreate,
    LiveYouTubeUpdate,
    LiveYouTubeOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)


def create_live_youtube(
    db: Session,
    payload: LiveYouTubeCreate,
) -> models.Asset:
    """
    Cria uma Live / YouTube Talk:
    - tipo_asset = live_youtube
    - plataforma = youtube
    """
    data = payload.model_dump()
    data.update(
        {
            "tipo_asset": TipoAssetEnum.live_youtube,
            "plataforma": PlataformaEnum.youtube,
        }
    )
    return create_asset(db, data)


def list_live_youtube(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[LiveYouTubeOut]:
    """
    Lista Lives / YouTube Talks com filtros opcionais:
    - formato: big_talk | one_talk | little_talk
    - campanha, cliente, search
    """
    items = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.live_youtube.value,
        plataforma=PlataformaEnum.youtube.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


def get_live_youtube(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    """
    Busca uma Live / YouTube Talk garantindo o tipo correto.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.live_youtube:
        return None
    return asset


def update_live_youtube(
    db: Session,
    asset_id: int,
    payload: LiveYouTubeUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza uma Live / YouTube Talk.
    Não permite trocar tipo_asset/plataforma.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.live_youtube:
        return None

    data = payload.model_dump(exclude_unset=True)
    # blindagem extra, se alguém tentar mandar:
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    updated = update_asset(db, asset, data)
    return updated


def delete_live_youtube(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta uma Live / YouTube Talk.
    Retorna:
    - True se deletou
    - False se não encontrou ou não era do tipo correto
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.live_youtube:
        return False

    delete_asset(db, asset_id)
    return True
