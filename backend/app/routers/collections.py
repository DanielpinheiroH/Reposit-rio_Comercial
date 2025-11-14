from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.post(
    "",
    response_model=schemas.CollectionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar coleção"
)
def create_collection(
    collection_in: schemas.CollectionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_collection(db, collection_in)


@router.get(
    "",
    response_model=List[schemas.CollectionOut],
    summary="Listar coleções"
)
def list_collections(db: Session = Depends(get_db)):
    return crud.list_collections(db)


@router.get(
    "/{collection_id}",
    response_model=schemas.CollectionWithAssets,
    summary="Obter coleção (com assets)"
)
def get_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = crud.get_collection(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada.")
    return collection


@router.post(
    "/{collection_id}/items",
    response_model=schemas.CollectionWithAssets,
    summary="Adicionar asset à coleção"
)
def add_item(
    collection_id: int,
    item: schemas.CollectionItemAdd,
    db: Session = Depends(get_db),
):
    collection = crud.get_collection(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada.")

    asset = crud.get_asset(db, item.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset não encontrado.")

    return crud.add_asset_to_collection(db, collection, asset)


@router.delete(
    "/{collection_id}/items/{asset_id}",
    response_model=schemas.CollectionWithAssets,
    summary="Remover asset da coleção"
)
def remove_item(
    collection_id: int,
    asset_id: int,
    db: Session = Depends(get_db),
):
    collection = crud.get_collection(db, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada.")

    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset não encontrado.")

    return crud.remove_asset_from_collection(db, collection, asset)
