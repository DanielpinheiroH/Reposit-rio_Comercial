# backend/app/routers/collections.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.collections import (
    CollectionCreate,
    CollectionOut,
    CollectionItemAdd,
    CollectionWithAssets,
)
from ..crud.collections import (
    create_collection as crud_create_collection,
    list_collections as crud_list_collections,
    get_collection_with_assets as crud_get_collection_with_assets,
    add_asset_to_collection as crud_add_asset_to_collection,
    remove_asset_from_collection as crud_remove_asset_from_collection,
)

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.post(
    "",
    response_model=CollectionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar coleção",
)
def create_collection(
    collection_in: CollectionCreate,
    db: Session = Depends(get_db),
):
    """
    Cria uma nova coleção (sem assets).
    """
    collection = crud_create_collection(db, collection_in)
    return collection


@router.get(
    "",
    response_model=List[CollectionOut],
    summary="Listar coleções",
)
def list_collections(
    db: Session = Depends(get_db),
):
    """
    Lista coleções cadastradas (sem carregar assets).
    """
    return crud_list_collections(db)


@router.get(
    "/{collection_id}",
    response_model=CollectionWithAssets,
    summary="Obter coleção (com assets)",
)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtém uma coleção específica com a lista de assets vinculados.
    """
    collection = crud_get_collection_with_assets(db, collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coleção não encontrada.",
        )
    return collection


@router.post(
    "/{collection_id}/items",
    response_model=CollectionWithAssets,
    status_code=status.HTTP_200_OK,
    summary="Adicionar asset à coleção",
)
def add_item(
    collection_id: int,
    item: CollectionItemAdd,
    db: Session = Depends(get_db),
):
    """
    Adiciona um asset à coleção e retorna a coleção com assets atualizada.
    """
    try:
        collection = crud_add_asset_to_collection(db, collection_id, item.asset_id)
    except ValueError as e:
        # Mensagens de erro já vêm descritivas do CRUD ("Coleção não encontrada." / "Asset não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return collection


@router.delete(
    "/{collection_id}/items/{asset_id}",
    response_model=CollectionWithAssets,
    summary="Remover asset da coleção",
)
def remove_item(
    collection_id: int,
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove um asset da coleção (idempotente) e retorna a coleção com assets atualizada.
    """
    try:
        collection = crud_remove_asset_from_collection(db, collection_id, asset_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    if not collection:
        # fallback defensivo (mas pela nossa lógica sempre volta algo se a coleção existir)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coleção não encontrada.",
        )

    return collection
