from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .asset_common import Plataforma


class MetricBase(BaseModel):
    plataforma: Plataforma
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    engagement: Optional[int] = None
    reach: Optional[int] = None
    raw_json: Optional[dict] = None


class MetricCreate(MetricBase):
    pass


class MetricOut(MetricBase):
    id: int
    asset_id: int
    capturado_em: datetime

    class Config:
        from_attributes = True
