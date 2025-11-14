from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from .. import models
from .assets_base import create_asset, get_asset, update_asset, delete_asset


def _coerce_enums(data: Dict[str, Any]) -> Dict[str, Any]:
    """Converte strings para Enums do SQLAlchemy quando presentes."""
    coerced = dict(data)

    if "tipo_asset" in coerced and isinstance(coerced["tipo_asset"], str):
        coerced["tipo_asset"] = models.TipoAssetEnum(coerced["tipo_asset"])

    if "plataforma" in coerced and isinstance(coerced["plataforma"], str):
        coerced["plataforma"] = models.PlataformaEnum(coerced["plataforma"])

    # formato é string; para testemunhal deve ser sempre "reels"
    if "formato" in coerced and coerced["formato"] is None:
        # deixar como None se update "limpando" não for desejado
        pass

    return coerced


def create_social_testemunhal(db: Session, data_dict: Dict[str, Any]) -> models.Asset:
    """
    Cria um Social Vídeo Testemunhal (instagram/tiktok, formato = 'reels').
    Espera campos comuns de Asset +:
      - tipo_asset = 'social_video_testemunhal'
      - plataforma in ['instagram', 'tiktok']
      - formato = 'reels'
      - duracao_seg in [30, 60] (opcional, validado no schema também)
    """
    # Garantias adicionais (além do schema)
    data_dict = dict(data_dict)
    data_dict["tipo_asset"] = "social_video_testemunhal"
    if data_dict.get("plataforma") not in ("instagram", "tiktok"):
        raise ValueError("Plataforma inválida. Use 'instagram' ou 'tiktok'.")
    data_dict["formato"] = "reels"

    # Converte para enums onde necessário
    data_dict = _coerce_enums(data_dict)
    return create_asset(db, data_dict)


def get_social_testemunhal(db: Session, asset_id: int) -> Optional[models.Asset]:
    return get_asset(db, asset_id)


def update_social_testemunhal(db: Session, asset: models.Asset, data_dict: Dict[str, Any]) -> models.Asset:
    """
    Atualiza campos do Testemunhal. Se vier plataforma, valida; se vier formato, força 'reels'.
    """
    data = dict(data_dict or {})

    if "plataforma" in data:
        if data["plataforma"] not in (None, "instagram", "tiktok"):
            raise ValueError("Plataforma inválida. Use 'instagram' ou 'tiktok'.")

    if "formato" in data:
        # sempre manter 'reels' se usuário tentar mudar
        data["formato"] = "reels"

    data = _coerce_enums(data)
    return update_asset(db, asset, data)


def delete_social_testemunhal(db: Session, asset_id: int) -> None:
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
    filters = [models.Asset.tipo_asset == models.TipoAssetEnum.social_video_testemunhal]

    if plataforma in ("instagram", "tiktok"):
        filters.append(models.Asset.plataforma == models.PlataformaEnum(plataforma))

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
