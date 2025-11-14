from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..crud import assets_base as crud
from ..schemas.conteudo_especial import (
    ConteudoEspecialCreate,
    ConteudoEspecialUpdate,
    ConteudoEspecialOut,
)

# Slugs aceitos (batendo com o schema acima)
FORMATS_ALLOWED = {
    "expressao_de_opiniao_digital",
    "publicidade_nativa",
    "publieditorial",
    "manchete",
    "sub_manchete",
}

router = APIRouter(prefix="/conteudo-especial", tags=["Conteúdo Especial"])


@router.get("", response_model=List[ConteudoEspecialOut])
def list_conteudos(
    search: Optional[str] = Query(None, description="Busca em título/descrição/campanha/cliente"),
    formato: Optional[str] = Query(None, description="expressao_de_opiniao_digital|publicidade_nativa|publieditorial|manchete|sub_manchete"),
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    if formato and formato not in FORMATS_ALLOWED:
        raise HTTPException(status_code=400, detail="formato inválido")

    items = crud.list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.conteudo_especial,
        plataforma=models.PlataformaEnum.site,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )
    return items


@router.post("", response_model=ConteudoEspecialOut, status_code=201)
def create_conteudo(payload: ConteudoEspecialCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    if data.get("formato") not in FORMATS_ALLOWED:
        raise HTTPException(status_code=400, detail="formato inválido")

    data.update(
        dict(
            tipo_asset=models.TipoAssetEnum.conteudo_especial,
            plataforma=models.PlataformaEnum.site,
        )
    )
    created = crud.create_asset(db, data)
    return created


@router.get("/{asset_id}", response_model=ConteudoEspecialOut)
def get_conteudo(asset_id: int, db: Session = Depends(get_db)):
    obj = crud.get_asset(db, asset_id)
    if not obj or obj.tipo_asset != models.TipoAssetEnum.conteudo_especial:
        raise HTTPException(status_code=404, detail="Conteúdo especial não encontrado")
    return obj


@router.put("/{asset_id}", response_model=ConteudoEspecialOut)
def update_conteudo(asset_id: int, payload: ConteudoEspecialUpdate, db: Session = Depends(get_db)):
    obj = crud.get_asset(db, asset_id)
    if not obj or obj.tipo_asset != models.TipoAssetEnum.conteudo_especial:
        raise HTTPException(status_code=404, detail="Conteúdo especial não encontrado")

    data = payload.model_dump(exclude_unset=True)
    if "formato" in data and data["formato"] and data["formato"] not in FORMATS_ALLOWED:
        raise HTTPException(status_code=400, detail="formato inválido")

    # mantém fixo plataforma/tipo
    data.update(dict(plataforma=models.PlataformaEnum.site))
    updated = crud.update_asset(db, obj, data)
    return updated


@router.delete("/{asset_id}", status_code=204)
def delete_conteudo(asset_id: int, db: Session = Depends(get_db)):
    obj = crud.get_asset(db, asset_id)
    if not obj or obj.tipo_asset != models.TipoAssetEnum.conteudo_especial:
        raise HTTPException(status_code=404, detail="Conteúdo especial não encontrado")
    crud.delete_asset(db, asset_id)
