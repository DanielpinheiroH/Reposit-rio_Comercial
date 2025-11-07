from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from .. import models


def create_asset(db: Session, data_dict: dict) -> models.Asset:
    """Cria um Asset genérico a partir de um dicionário de dados."""
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
        filters.append(models.Asset.tipo_asset == tipo_asset)
    if plataforma:
        filters.append(models.Asset.plataforma == plataforma)
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
