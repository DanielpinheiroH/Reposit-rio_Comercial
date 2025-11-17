from typing import List, Optional, Dict, Any

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.social_testemunhal import (
    SocialTestemunhalCreate,
    SocialTestemunhalUpdate,
    SocialTestemunhalOut,
)
from .assets_base import create_asset, get_asset, update_asset, delete_asset


def _coerce_enums(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte strings para Enums do SQLAlchemy quando presentes.
    Usado como proteção extra caso algum dado chegue "cru".
    """
    coerced = dict(data)

    if "tipo_asset" in coerced and isinstance(coerced["tipo_asset"], str):
        coerced["tipo_asset"] = TipoAssetEnum(coerced["tipo_asset"])

    if "plataforma" in coerced and isinstance(coerced["plataforma"], str):
        coerced["plataforma"] = PlataformaEnum(coerced["plataforma"])

    # formato continua string, para testemunhal sempre "reels"
    return coerced


def create_social_testemunhal(
    db: Session,
    payload: SocialTestemunhalCreate,
) -> models.Asset:
    """
    Cria um Social Vídeo Testemunhal (instagram/tiktok, formato='reels').

    Espera campos comuns de Asset +:
      - tipo_asset = 'social_video_testemunhal'
      - plataforma ∈ {'instagram', 'tiktok'}
      - formato = 'reels'
      - duracao_seg ∈ {30, 60} (validado no schema)
    """
    data_dict = payload.model_dump()

    # Garantias adicionais (além do schema)
    if data_dict.get("plataforma") not in ("instagram", "tiktok"):
        raise ValueError("Plataforma inválida. Use 'instagram' ou 'tiktok'.")

    data_dict["tipo_asset"] = TipoAssetEnum.social_video_testemunhal
    data_dict["plataforma"] = PlataformaEnum(data_dict["plataforma"])
    data_dict["formato"] = "reels"

    data_dict = _coerce_enums(data_dict)
    return create_asset(db, data_dict)


def get_social_testemunhal(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    return get_asset(db, asset_id)


def update_social_testemunhal(
    db: Session,
    asset_id: int,
    payload: SocialTestemunhalUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza campos do Testemunhal.
    - Se vier plataforma, valida ('instagram' ou 'tiktok').
    - Se vier formato, força 'reels'.
    """
    asset = get_asset(db, asset_id)
    if not asset or asset.tipo_asset != TipoAssetEnum.social_video_testemunhal:
        return None

    data = dict(payload.model_dump(exclude_unset=True) or {})

    if "plataforma" in data and data["plataforma"] is not None:
        if data["plataforma"] not in ("instagram", "tiktok"):
            raise ValueError("Plataforma inválida. Use 'instagram' ou 'tiktok'.")
        data["plataforma"] = PlataformaEnum(data["plataforma"])

    if "formato" in data:
        # sempre manter 'reels' se usuário tentar mudar
        data["formato"] = "reels"

    data = _coerce_enums(data)
    updated = update_asset(db, asset, data)
    return updated


def delete_social_testemunhal(
    db: Session,
    asset_id: int,
) -> None:
    delete_asset(db, asset_id)


def list_social_testemunhal(
    db: Session,
    plataforma: Optional[str] = None,   # 'instagram' | 'tiktok' | None
    duracao_seg: Optional[int] = None,  # 30 | 60 | None
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """
    Lista Testemunhais com filtros simples.
    """
    filters = [models.Asset.tipo_asset == TipoAssetEnum.social_video_testemunhal]

    if plataforma in ("instagram", "tiktok"):
        filters.append(models.Asset.plataforma == PlataformaEnum(plataforma))

    if duracao_seg in (30, 60):
        filters.append(models.Asset.duracao_seg == duracao_seg)

    if search:
        like = f"%{search}%"
        filters.append(
            (models.Asset.titulo.ilike(like))
            | (models.Asset.descricao.ilike(like))
            | (models.Asset.campanha.ilike(like))
            | (models.Asset.cliente.ilike(like))
        )

    stmt = (
        select(models.Asset)
        .where(and_(*filters))
        .order_by(
            models.Asset.data_publicacao.desc().nullslast(),
            models.Asset.id.desc(),
        )
        .offset(skip)
        .limit(limit)
    )

    return db.execute(stmt).scalars().all()
