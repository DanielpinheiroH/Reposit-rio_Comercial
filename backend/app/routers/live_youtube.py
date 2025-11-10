from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/lives", tags=["Lives YouTube"])


@router.post("", response_model=schemas.LiveYoutubeOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.LiveYoutubeCreate, db: Session = Depends(get_db)):
    return crud.create_live_youtube(db, data)


@router.get("", response_model=List[schemas.LiveYoutubeOut])
def list_lives(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_live_youtube(db, search=search, skip=skip, limit=limit)
