from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from ..database import get_db
from .. import models
from ..schemas.metrics import MetricCreate, MetricUpdate, MetricOut

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/", response_model=MetricOut, status_code=201)
def create_metric(payload: MetricCreate, db: Session = Depends(get_db)):
    # valida asset
    asset = db.get(models.Asset, payload.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset não encontrado")

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

@router.get("/", response_model=List[MetricOut])
def list_metrics(
    db: Session = Depends(get_db),
    asset_id: Optional[int] = Query(None, ge=1),
    plataforma: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    filters = []
    if asset_id:
        filters.append(models.Metric.asset_id == asset_id)
    if plataforma:
        filters.append(models.Metric.plataforma == plataforma)

    stmt = select(models.Metric).order_by(models.Metric.capturado_em.desc())
    if filters:
        stmt = stmt.where(and_(*filters))
    stmt = stmt.offset(skip).limit(limit)

    return db.execute(stmt).scalars().all()

@router.get("/{metric_id}", response_model=MetricOut)
def get_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.get(models.Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    return metric

@router.put("/{metric_id}", response_model=MetricOut)
def update_metric(metric_id: int, payload: MetricUpdate, db: Session = Depends(get_db)):
    metric = db.get(models.Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(metric, k, v)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.delete("/{metric_id}", status_code=204)
def delete_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.get(models.Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    db.delete(metric)
    db.commit()
