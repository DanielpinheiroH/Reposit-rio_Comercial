# backend/app/routers/metrics.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.metrics import (
    create_metric as crud_create_metric,
    list_metrics as crud_list_metrics,
    get_metric as crud_get_metric,
    update_metric as crud_update_metric,
    delete_metric as crud_delete_metric,
)
from ..schemas.metrics import (
    MetricCreate,
    MetricUpdate,
    MetricOut,
)

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.post("/", response_model=MetricOut, status_code=201)
def create_metric(
    payload: MetricCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um registro de métricas para um asset.
    """
    try:
        metric = crud_create_metric(db, payload)
    except ValueError as e:
        # Hoje o único ValueError vem de "Asset não encontrado"
        raise HTTPException(status_code=404, detail=str(e))
    return metric


@router.get("/", response_model=List[MetricOut])
def list_metrics(
    db: Session = Depends(get_db),
    asset_id: Optional[int] = Query(None, ge=1),
    plataforma: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Lista métricas com filtros opcionais.
    """
    metrics = crud_list_metrics(
        db=db,
        asset_id=asset_id,
        plataforma=plataforma,
        skip=skip,
        limit=limit,
    )
    return metrics


@router.get("/{metric_id}", response_model=MetricOut)
def get_metric(
    metric_id: int,
    db: Session = Depends(get_db),
):
    """
    Detalhe de uma métrica específica.
    """
    metric = crud_get_metric(db, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    return metric


@router.put("/{metric_id}", response_model=MetricOut)
def update_metric(
    metric_id: int,
    payload: MetricUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza uma métrica.
    """
    metric = crud_update_metric(db, metric_id, payload)
    if not metric:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    return metric


@router.delete("/{metric_id}", status_code=204)
def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta uma métrica.
    """
    success = crud_delete_metric(db, metric_id)
    if not success:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    return None
