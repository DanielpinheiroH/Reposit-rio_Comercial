from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/posts/tiktok", tags=["Posts TikTok"])


@router.post("", response_model=schemas.TikTokPostOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.TikTokPostCreate, db: Session = Depends(get_db)):
    return crud.create_tiktok_post(db, data)


@router.get("", response_model=List[schemas.TikTokPostOut])
def list_posts(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_tiktok_posts(db, search=search, skip=skip, limit=limit)
