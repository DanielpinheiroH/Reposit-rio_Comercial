# backend/app/routers/conteudo_especial.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud.conteudo_especial import (
    create_conteudo_especial as crud_create_conteudo_especial,
    list_conteudo_especial as crud_list_conteudo_especial,
    get_conteudo_especial as crud_get_conteudo_especial,
    update_conteudo_especial as crud_update_conteudo_especial,
    delete_conteudo_especial as crud_delete_conteudo_especial,
    FORMATS_ALLOWED,
)
from ..schemas.conteudo_especial import (
    ConteudoEspecialCreate,
    ConteudoEspecialUpdate,
    ConteudoEspecialOut,
)

router = APIRouter(prefix="/conteudo-especial", tags=["Conteúdo Especial"])


@router.get("", response_model=List[ConteudoEspecialOut])
def list_conteudos(
    search: Optional[str] = Query(
        None,
        description="Busca em título/descrição/campanha/cliente",
    ),
    formato: Optional[str] = Query(
        None,
        description=(
            "expressao_de_opiniao_digital|publicidade_nativa|publieditorial|"
            "manchete|sub_manchete"
        ),
    ),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """
    Lista Conteúdos Especiais com filtros opcionais.
    """
    if formato and formato not in FORMATS_ALLOWED:
        raise HTTPException(status_code=400, detail="formato inválido")

    items = crud_list_conteudo_especial(
        db=db,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


@router.post("", response_model=ConteudoEspecialOut, status_code=201)
def create_conteudo(
    payload: ConteudoEspecialCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um Conteúdo Especial.
    """
    data = payload.model_dump()
    if data.get("formato") not in FORMATS_ALLOWED:
        raise HTTPException(status_code=400, detail="formato inválido")

    created = crud_create_conteudo_especial(db, payload)
    return created


@router.get("/{asset_id}", response_model=ConteudoEspecialOut)
def get_conteudo(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Detalhe de um Conteúdo Especial.
    """
    obj = crud_get_conteudo_especial(db, asset_id)
    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Conteúdo especial não encontrado",
        )
    return obj


@router.put("/{asset_id}", response_model=ConteudoEspecialOut)
def update_conteudo(
    asset_id: int,
    payload: ConteudoEspecialUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza um Conteúdo Especial.
    """
    data = payload.model_dump(exclude_unset=True)
    if "formato" in data and data["formato"] and data["formato"] not in FORMATS_ALLOWED:
        raise HTTPException(status_code=400, detail="formato inválido")

    updated = crud_update_conteudo_especial(db, asset_id, payload)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Conteúdo especial não encontrado",
        )
    return updated


@router.delete("/{asset_id}", status_code=204)
def delete_conteudo(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Deleta um Conteúdo Especial.
    """
    success = crud_delete_conteudo_especial(db, asset_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Conteúdo especial não encontrado",
        )
    return None
