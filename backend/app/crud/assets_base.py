# backend/app/crud/assets_base.py

from typing import List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from .. import models

# -------------------------
# Tipos auxiliares
# -------------------------

TipoAssetLike = Union[str, models.TipoAssetEnum, None]
PlataformaLike = Union[str, models.PlataformaEnum, None]

# -------------------------
# Auxiliares de coerção/validação
# -------------------------

# Mapa de formatos sugeridos por tipo/plataforma (não é obrigatório, apenas ajuda a padronizar)
SUGGESTED_FORMATS: Dict[str, Dict[str, List[str]]] = {
    # YouTube Talks
    models.TipoAssetEnum.youtube_talk.value: {
        models.PlataformaEnum.youtube.value: ["big_talk", "one_talk", "little_talk"],
    },
    # Instagram
    models.TipoAssetEnum.post_instagram.value: {
        models.PlataformaEnum.instagram.value: ["fixado_feed", "feed", "stories", "reels"],
    },
    # Shorts
    models.TipoAssetEnum.post_youtube_shorts.value: {
        models.PlataformaEnum.youtube_shorts.value: ["shorts"],
    },
    # TikTok/Kwai/Facebook feed
    models.TipoAssetEnum.post_tiktok.value: {
        models.PlataformaEnum.tiktok.value: ["feed"],
    },
    models.TipoAssetEnum.post_kwai.value: {
        models.PlataformaEnum.kwai.value: ["feed"],
    },
    models.TipoAssetEnum.post_facebook.value: {
        models.PlataformaEnum.facebook.value: ["feed"],
    },
    # Testemunhal social (30s/60s) — pode aparecer em várias plataformas
    models.TipoAssetEnum.social_video_testemunhal.value: {
        models.PlataformaEnum.instagram.value: ["30s", "60s"],
        models.PlataformaEnum.tiktok.value: ["30s", "60s"],
        models.PlataformaEnum.kwai.value: ["30s", "60s"],
        models.PlataformaEnum.youtube_shorts.value: ["30s", "60s"],
        models.PlataformaEnum.facebook.value: ["30s", "60s"],
        models.PlataformaEnum.youtube.value: ["30s", "60s"],
    },
}


def _to_enum(enum_cls: Any, value: Optional[Any]) -> Optional[Any]:
    """Converte string ou enum-instance em Enum alvo com segurança; retorna None se não casar."""
    if value is None:
        return None
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(value)
    except Exception:
        return None


def _sanitize_formato(
    tipo_asset: Optional[str],
    plataforma: Optional[str],
    formato: Optional[str],
) -> Optional[str]:
    """
    Normaliza 'formato':
    - trim, lower, troca espaços por underscore;
    - converte 30/30seg/30s → 30s, 60/60seg/60s → 60s;
    - se existir sugestão para (tipo, plataforma), a UI pode se beneficiar, mas aqui não bloqueamos.
    """
    if not formato:
        return None

    f = str(formato).strip()
    if not f:
        return None

    # Normalização simples
    norm = f.lower().replace(" ", "_").replace('"', "").replace("''", "")

    # 30", 60" → 30s, 60s
    if norm in {"30", "30seg", "30s"}:
        norm = "30s"
    elif norm in {"60", "60seg", "60s"}:
        norm = "60s"

    tipo_key = (tipo_asset or "").strip()
    plat_key = (plataforma or "").strip()

    if tipo_key in SUGGESTED_FORMATS and plat_key in SUGGESTED_FORMATS[tipo_key]:
        # Poderíamos validar aqui e restringir, mas a ideia deste core é ser permissivo.
        # Deixamos a validação dura para os CRUDs específicos / schemas Pydantic.
        pass

    return norm


# -------------------------
# CRUD Genérico de Asset
# -------------------------

def create_asset(db: Session, data_dict: Dict[str, Any]) -> models.Asset:
    """Cria um Asset genérico a partir de um dicionário de dados."""

    # Coerção segura de enums (se vierem como string)
    if "tipo_asset" in data_dict:
        coerced = _to_enum(models.TipoAssetEnum, data_dict.get("tipo_asset"))
        if coerced:
            data_dict["tipo_asset"] = coerced

    if "plataforma" in data_dict:
        coerced = _to_enum(models.PlataformaEnum, data_dict.get("plataforma"))
        if coerced:
            data_dict["plataforma"] = coerced

    if "classificacao_conteudo_especial" in data_dict:
        coerced = _to_enum(
            models.ClassConteudoEnum,
            data_dict.get("classificacao_conteudo_especial"),
        )
        if coerced:
            data_dict["classificacao_conteudo_especial"] = coerced

    # Sanitiza formato (opcional, não bloqueante)
    tipo_val = data_dict.get("tipo_asset")
    plat_val = data_dict.get("plataforma")

    tipo_str = (
        tipo_val.value
        if isinstance(tipo_val, models.TipoAssetEnum)
        else (str(tipo_val) if tipo_val is not None else None)
    )
    plat_str = (
        plat_val.value
        if isinstance(plat_val, models.PlataformaEnum)
        else (str(plat_val) if plat_val is not None else None)
    )

    data_dict["formato"] = _sanitize_formato(
        tipo_str,
        plat_str,
        data_dict.get("formato"),
    )

    asset = models.Asset(**data_dict)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def get_asset(db: Session, asset_id: int) -> Optional[models.Asset]:
    """Busca um asset pelo ID."""
    return db.get(models.Asset, asset_id)


def update_asset(db: Session, asset: models.Asset, data_dict: Dict[str, Any]) -> models.Asset:
    """Atualiza campos de um asset existente."""

    # Coerção de enums, se vierem no payload
    if "tipo_asset" in data_dict:
        coerced = _to_enum(models.TipoAssetEnum, data_dict.get("tipo_asset"))
        if coerced:
            data_dict["tipo_asset"] = coerced

    if "plataforma" in data_dict:
        coerced = _to_enum(models.PlataformaEnum, data_dict.get("plataforma"))
        if coerced:
            data_dict["plataforma"] = coerced

    if "classificacao_conteudo_especial" in data_dict:
        coerced = _to_enum(
            models.ClassConteudoEnum,
            data_dict.get("classificacao_conteudo_especial"),
        )
        if coerced:
            data_dict["classificacao_conteudo_especial"] = coerced

    # Se qualquer uma dessas informações mexeu, recalculamos formato
    if "formato" in data_dict or "tipo_asset" in data_dict or "plataforma" in data_dict:
        tipo_val = data_dict.get("tipo_asset", getattr(asset, "tipo_asset", None))
        plat_val = data_dict.get("plataforma", getattr(asset, "plataforma", None))

        tipo_str = (
            tipo_val.value
            if isinstance(tipo_val, models.TipoAssetEnum)
            else (str(tipo_val) if tipo_val is not None else None)
        )
        plat_str = (
            plat_val.value
            if isinstance(plat_val, models.PlataformaEnum)
            else (str(plat_val) if plat_val is not None else None)
        )

        data_dict["formato"] = _sanitize_formato(
            tipo_str,
            plat_str,
            data_dict.get("formato", getattr(asset, "formato", None)),
        )

    # Aplica todos os campos
    for field, value in data_dict.items():
        setattr(asset, field, value)

    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset_id: int) -> None:
    """Remove um asset pelo ID, se existir."""
    asset = get_asset(db, asset_id)
    if asset:
        db.delete(asset)
        db.commit()


def list_assets(
    db: Session,
    tipo_asset: TipoAssetLike = None,
    plataforma: PlataformaLike = None,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """
    Lista assets com filtros genéricos, usado pelos CRUDs específicos.

    Observação: aceita tanto strings quanto Enums em tipo_asset/plataforma.
    """
    filters = []

    if tipo_asset:
        enum_val = _to_enum(models.TipoAssetEnum, tipo_asset)
        if enum_val:
            filters.append(models.Asset.tipo_asset == enum_val)

    if plataforma:
        enum_val = _to_enum(models.PlataformaEnum, plataforma)
        if enum_val:
            filters.append(models.Asset.plataforma == enum_val)

    if formato:
        filters.append(models.Asset.formato == formato)

    if campanha:
        filters.append(models.Asset.campanha.ilike(f"%{campanha}%"))

    if cliente:
        filters.append(models.Asset.cliente.ilike(f"%{cliente}%"))

    if search:
        like = f"%{search}%"
        filters.append(
            (models.Asset.titulo.ilike(like))
            | (models.Asset.descricao.ilike(like))
            | (models.Asset.campanha.ilike(like))
            | (models.Asset.cliente.ilike(like))
        )

    stmt = select(models.Asset)
    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.order_by(
        models.Asset.data_publicacao.desc().nullslast(),
        models.Asset.id.desc(),
    )
    stmt = stmt.offset(skip).limit(limit)

    return db.execute(stmt).scalars().all()
