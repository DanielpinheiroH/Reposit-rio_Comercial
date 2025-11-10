from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models
from ..schemas import (
    CollectionCreate,
    CollectionOut,
    CollectionItemAdd,
    CollectionWithAssets,
)


def create_collection(db: Session, data: CollectionCreate) -> models.Collection:
    collection = models.Collection(
        nome=data.nome,
        descricao=data.descricao,
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


def get_collection(db: Session, collection_id: int) -> Optional[models.Collection]:
    return db.query(models.Collection).filter(models.Collection.id == collection_id).first()


def list_collections(
    db: Session,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Collection]:
    return (
        db.query(models.Collection)
        .order_by(models.Collection.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def add_asset_to_collection(db: Session, data: CollectionItemAdd) -> None:
    # assumindo tabela de relação CollectionAsset(collection_id, asset_id)
    exists = (
        db.query(models.CollectionAsset)
        .filter(
            models.CollectionAsset.collection_id == data.collection_id,
            models.CollectionAsset.asset_id == data.asset_id,
        )
        .first()
    )
    if exists:
        return

    link = models.CollectionAsset(
        collection_id=data.collection_id,
        asset_id=data.asset_id,
    )
    db.add(link)
    db.commit()


def get_collection_with_assets(
    db: Session, collection_id: int
) -> Optional[CollectionWithAssets]:
    collection = (
        db.query(models.Collection)
        .filter(models.Collection.id == collection_id)
        .first()
    )

    if not collection:
        return None

    asset_ids = (
        db.query(models.CollectionAsset.asset_id)
        .filter(models.CollectionAsset.collection_id == collection_id)
        .all()
    )
    asset_ids = [a[0] for a in asset_ids]

    return CollectionWithAssets(
        id=collection.id,
        nome=collection.nome,
        descricao=collection.descricao,
        created_at=collection.created_at,
        assets=asset_ids,
    )
def remove_asset_from_collection(db: Session, data: CollectionItemAdd) -> None:
    link = (
        db.query(models.CollectionAsset)
        .filter(
            models.CollectionAsset.collection_id == data.collection_id,
            models.CollectionAsset.asset_id == data.asset_id,
        )
        .first()
    )
    if not link:
        return

    db.delete(link)
    db.commit()