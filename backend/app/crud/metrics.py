# backend/app/crud/metrics.py

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from .. import models
from ..schemas.metrics import MetricCreate, MetricUpdate


def create_metric(
    db: Session,
    payload: MetricCreate,
) -> models.Metric:
    """
    Cria um registro de métricas para um asset.
    Valida se o asset existe antes.
    """
    asset = db.get(models.Asset, payload.asset_id)
    if not asset:
        # Deixamos a camada de API decidir o status HTTP,
        # aqui só sinalizamos erro de domínio.
        raise ValueError("Asset não encontrado")

    metric = models.Metric(
        asset_id=payload.asset_id,
        plataforma=payload.plataforma,  # compatível com Enum (Pydantic converte)
        views=payload.views,
        likes=payload.likes,
        comments=payload.comments,
        shares=payload.shares,
        engagement=payload.engagement,
        reach=payload.reach,
        raw_json=payload.raw_json,
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def list_metrics(
    db: Session,
    asset_id: Optional[int] = None,
    plataforma: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Metric]:
    """
    Lista métricas com filtros opcionais:
    - asset_id
    - plataforma
    - paginação (skip, limit)
    """
    filters = []

    if asset_id:
        filters.append(models.Metric.asset_id == asset_id)

    if plataforma:
        # Dependendo de como o Enum foi configurado, comparar com string funciona.
        # Se preferir, pode trocar para models.PlataformaEnum(plataforma).
        filters.append(models.Metric.plataforma == plataforma)

    stmt = select(models.Metric).order_by(models.Metric.capturado_em.desc())
    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def list_metrics_by_asset(
    db: Session,
    asset_id: int,
    limit: int = 100,
) -> List[models.Metric]:
    """
    Atalho para listar métricas de um único asset, limitado.
    (Mantém assinatura parecida com a que você já tinha.)
    """
    return list_metrics(db, asset_id=asset_id, limit=limit)


def get_metric(
    db: Session,
    metric_id: int,
) -> Optional[models.Metric]:
    """
    Busca uma métrica pelo ID.
    """
    return db.get(models.Metric, metric_id)


def update_metric(
    db: Session,
    metric_id: int,
    payload: MetricUpdate,
) -> Optional[models.Metric]:
    """
    Atualiza uma métrica.
    Retorna None se não encontrar.
    """
    metric = db.get(models.Metric, metric_id)
    if not metric:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(metric, k, v)

    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def delete_metric(
    db: Session,
    metric_id: int,
) -> bool:
    """
    Deleta uma métrica.
    Retorna:
    - True se deletou
    - False se não encontrou.
    """
    metric = db.get(models.Metric, metric_id)
    if not metric:
        return False

    db.delete(metric)
    db.commit()
    return True
