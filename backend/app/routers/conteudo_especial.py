from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/conteudo-especial", tags=["Conteúdo Especial"])


@router.post("", response_model=schemas.ConteudoEspecialOut, status_code=status.HTTP_201_CREATED)
def create(data: schemas.ConteudoEspecialCreate, db: Session = Depends(get_db)):
    asset = crud.create_conteudo_especial(db, data)
    return asset


@router.get("", response_model=List[schemas.ConteudoEspecialOut])
def list_conteudo_especial(
    db: Session = Depends(get_db),
    classificacao: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return crud.list_conteudo_especial(
        db,
        classificacao=classificacao,
        search=search,
        skip=skip,
        limit=limit,
    )
