from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/assets/{asset_id}/metrics", tags=["Metrics"])


@router.post("", response_model=schemas.MetricOut, status_code=status.HTTP_201_CREATED)
def create_metric_for_asset(
    asset_id: int,
    metric_in: schemas.MetricCreate,
    db: Session = Depends(get_db),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset não encontrado.")
    return crud.create_metric(db, asset_id, metric_in)


@router.get("", response_model=List[schemas.MetricOut])
def list_metrics_for_asset(
    asset_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset não encontrado.")
    return crud.list_metrics_by_asset(db, asset_id, limit=limit)
