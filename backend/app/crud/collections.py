# backend/app/crud/collections.py

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models
from ..schemas.collections import (
    CollectionCreate,
    CollectionItemAdd,
    CollectionWithAssets,
)
from ..schemas.asset_common import AssetOutCommon


def create_collection(db: Session, data: CollectionCreate) -> models.Collection:
    """
    Cria uma coleção simples (sem assets).
    """
    collection = models.Collection(
        nome=data.nome,
        descricao=data.descricao,
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


def get_collection(db: Session, collection_id: int) -> Optional[models.Collection]:
    """
    Retorna a Collection ORM (sem montagem de assets).
    """
    return (
        db.query(models.Collection)
        .filter(models.Collection.id == collection_id)
        .first()
    )


def list_collections(
    db: Session,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Collection]:
    """
    Lista coleções, sem carregar assets (para listagem básica).
    """
    return (
        db.query(models.Collection)
        .order_by(models.Collection.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def _load_collection_assets(
    db: Session, collection_id: int
) -> List[models.Asset]:
    """
    Busca os Assets vinculados à coleção via tabela de associação CollectionAsset.
    """
    asset_ids_rows = (
        db.query(models.CollectionAsset.asset_id)
        .filter(models.CollectionAsset.collection_id == collection_id)
        .all()
    )
    asset_ids = [row[0] for row in asset_ids_rows]

    if not asset_ids:
        return []

    assets = (
        db.query(models.Asset)
        .filter(models.Asset.id.in_(asset_ids))
        .all()
    )
    return assets


def get_collection_with_assets(
    db: Session, collection_id: int
) -> Optional[CollectionWithAssets]:
    """
    Retorna a coleção + lista de assets já no formato CollectionWithAssets.
    """
    collection = get_collection(db, collection_id)
    if not collection:
        return None

    assets = _load_collection_assets(db, collection_id)

    return CollectionWithAssets(
        id=collection.id,
        nome=collection.nome,
        descricao=collection.descricao,
        created_at=collection.created_at,
        updated_at=collection.updated_at,
        assets=[AssetOutCommon.model_validate(a) for a in assets],
    )


def add_asset_to_collection(
    db: Session,
    collection_id: int,
    asset_id: int,
) -> CollectionWithAssets:
    """
    Adiciona um asset à coleção (idempotente) e retorna a coleção com assets.
    Lança ValueError se coleção ou asset não existirem.
    """
    collection = get_collection(db, collection_id)
    if not collection:
        raise ValueError("Coleção não encontrada.")

    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise ValueError("Asset não encontrado.")

    # Verifica se já existe o vínculo
    exists = (
        db.query(models.CollectionAsset)
        .filter(
            models.CollectionAsset.collection_id == collection_id,
            models.CollectionAsset.asset_id == asset_id,
        )
        .first()
    )
    if not exists:
        link = models.CollectionAsset(
            collection_id=collection_id,
            asset_id=asset_id,
        )
        db.add(link)
        db.commit()

    # Retorna a coleção atualizada com assets completos
    return get_collection_with_assets(db, collection_id)


def remove_asset_from_collection(
    db: Session,
    collection_id: int,
    asset_id: int,
) -> CollectionWithAssets:
    """
    Remove um asset da coleção (idempotente) e retorna a coleção com assets.
    Lança ValueError se coleção não existir.
    """
    collection = get_collection(db, collection_id)
    if not collection:
        raise ValueError("Coleção não encontrada.")

    # Se o asset não existir, podemos tratar como erro ou ignorar;
    # aqui checamos para dar erro mais claro.
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise ValueError("Asset não encontrado.")

    link = (
        db.query(models.CollectionAsset)
        .filter(
            models.CollectionAsset.collection_id == collection_id,
            models.CollectionAsset.asset_id == asset_id,
        )
        .first()
    )
    if link:
        db.delete(link)
        db.commit()

    # Mesmo se não existia link, retornamos o estado atual da coleção
    return get_collection_with_assets(db, collection_id)
