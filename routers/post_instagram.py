from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/posts/instagram", tags=["Posts Instagram"])


@router.post("", response_model=schemas.InstagramPostOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.InstagramPostCreate, db: Session = Depends(get_db)):
    return crud.create_instagram_post(db, data)


@router.get("", response_model=List[schemas.InstagramPostOut])
def list_posts(
    db: Session = Depends(get_db),
    formato: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_instagram_posts(
        db,
        formato=formato,
        search=search,
        skip=skip,
        limit=limit,
    )
