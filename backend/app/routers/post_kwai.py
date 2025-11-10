from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/posts/kwai", tags=["Posts Kwai"])


@router.post("", response_model=schemas.KwaiPostOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.KwaiPostCreate, db: Session = Depends(get_db)):
    return crud.create_kwai_post(db, data)


@router.get("", response_model=List[schemas.KwaiPostOut])
def list_posts(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_kwai_posts(db, search=search, skip=skip, limit=limit)
