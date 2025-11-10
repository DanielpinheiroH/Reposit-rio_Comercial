from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/posts/youtube-shorts", tags=["YouTube Shorts"])


@router.post("", response_model=schemas.YoutubeShortsOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.YoutubeShortsCreate, db: Session = Depends(get_db)):
    return crud.create_youtube_shorts(db, data)


@router.get("", response_model=List[schemas.YoutubeShortsOut])
def list_posts(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_youtube_shorts(db, search=search, skip=skip, limit=limit)
