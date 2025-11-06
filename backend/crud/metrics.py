from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import models, schemas


def create_metric(
    db: Session,
    asset_id: int,
    data: schemas.MetricCreate,
) -> models.Metric:
    obj = models.Metric(
        asset_id=asset_id,
        **data.model_dump(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_metrics_by_asset(
    db: Session,
    asset_id: int,
    limit: int = 100,
) -> List[models.Metric]:
    stmt = (
        select(models.Metric)
        .where(models.Metric.asset_id == asset_id)
        .order_by(models.Metric.capturado_em.desc())
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()
