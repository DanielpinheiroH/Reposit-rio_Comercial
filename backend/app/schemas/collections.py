from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from .asset_common import AssetOutCommon


class CollectionBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class CollectionCreate(CollectionBase):
    pass


class CollectionOut(CollectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CollectionItemAdd(BaseModel):
    asset_id: int


class CollectionWithAssets(CollectionOut):
    assets: List[AssetOutCommon] = []
