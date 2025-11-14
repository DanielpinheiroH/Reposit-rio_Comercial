from typing import List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from .. import models

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


def _to_enum(enum_cls: Any, value: Optional[str]) -> Optional[Any]:
    """Converte string em Enum com segurança; retorna None se não casar."""
    if value is None:
        return None
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(value)
    except Exception:
        return None


def _sanitize_formato(tipo_asset: Optional[str], plataforma: Optional[str], formato: Optional[str]) -> Optional[str]:
    """
    Se existir sugestão de formato para (tipo, plataforma), e o formato informado não estiver
    na lista, mantém original (não bloquear). Apenas normaliza espaços e minúsculas.
    """
    if not formato:
        return None
    f = str(formato).strip()
    if not f:
        return None

    # normalização simples
    norm = f.lower().replace(" ", "_").replace('"', "").replace("''", "")
    # ex: 30", 60" -> 30s, 60s
    if norm in {"30", "30seg", "30s"}:
        norm = "30s"
    elif norm in {"60", "60seg", "60s"}:
        norm = "60s"

    # se houver lista sugerida, a UI pode se beneficiar (mas não bloqueamos)
    tipo_key = tipo_asset or ""
    plat_key = plataforma or ""
    if tipo_key in SUGGESTED_FORMATS and plat_key in SUGGESTED_FORMATS[tipo_key]:
        # poderíamos validar aqui; manteremos apenas a normalização
        pass

    return norm


# -------------------------
# CRUD Genérico
# -------------------------

def create_asset(db: Session, data_dict: dict) -> models.Asset:
    """Cria um Asset genérico a partir de um dicionário de dados."""
    # coerção segura de enums (se vierem como string)
    if "tipo_asset" in data_dict:
        coerced = _to_enum(models.TipoAssetEnum, data_dict.get("tipo_asset"))
        if coerced:
            data_dict["tipo_asset"] = coerced
    if "plataforma" in data_dict:
        coerced = _to_enum(models.PlataformaEnum, data_dict.get("plataforma"))
        if coerced:
            data_dict["plataforma"] = coerced
    if "classificacao_conteudo_especial" in data_dict:
        coerced = _to_enum(models.ClassConteudoEnum, data_dict.get("classificacao_conteudo_especial"))
        if coerced:
            data_dict["classificacao_conteudo_especial"] = coerced

    # sanitiza formato (opcional, não bloqueante)
    data_dict["formato"] = _sanitize_formato(
        str(data_dict.get("tipo_asset").value if isinstance(data_dict.get("tipo_asset"), models.TipoAssetEnum) else data_dict.get("tipo_asset")),
        str(data_dict.get("plataforma").value if isinstance(data_dict.get("plataforma"), models.PlataformaEnum) else data_dict.get("plataforma")),
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


def update_asset(db: Session, asset: models.Asset, data_dict: dict) -> models.Asset:
    """Atualiza campos de um asset existente."""
    if "tipo_asset" in data_dict:
        coerced = _to_enum(models.TipoAssetEnum, data_dict.get("tipo_asset"))
        if coerced:
            data_dict["tipo_asset"] = coerced
    if "plataforma" in data_dict:
        coerced = _to_enum(models.PlataformaEnum, data_dict.get("plataforma"))
        if coerced:
            data_dict["plataforma"] = coerced
    if "classificacao_conteudo_especial" in data_dict:
        coerced = _to_enum(models.ClassConteudoEnum, data_dict.get("classificacao_conteudo_especial"))
        if coerced:
            data_dict["classificacao_conteudo_especial"] = coerced

    if "formato" in data_dict or "tipo_asset" in data_dict or "plataforma" in data_dict:
        tipo_val = data_dict.get("tipo_asset", getattr(asset, "tipo_asset", None))
        plat_val = data_dict.get("plataforma", getattr(asset, "plataforma", None))
        tipo_str = tipo_val.value if isinstance(tipo_val, models.TipoAssetEnum) else tipo_val
        plat_str = plat_val.value if isinstance(plat_val, models.PlataformaEnum) else plat_val
        data_dict["formato"] = _sanitize_formato(tipo_str, plat_str, data_dict.get("formato", getattr(asset, "formato", None)))

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
    tipo_asset: Optional[str] = None,
    plataforma: Optional[str] = None,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    """Lista assets com filtros genéricos, usado pelos CRUDs específicos."""
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
