from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/social-testemunhal", tags=["Social Testemunhal"])


@router.post("", response_model=schemas.SocialTestemunhalOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.SocialTestemunhalCreate, db: Session = Depends(get_db)):
    return crud.create_social_testemunhal(db, data)


@router.get("", response_model=List[schemas.SocialTestemunhalOut])
def list_itens(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_social_testemunhal(db, search=search, skip=skip, limit=limit)
