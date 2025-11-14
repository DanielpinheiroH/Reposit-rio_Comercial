from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .asset_common import PlataformaLiteral  # se preferir, pode remover e usar str

class MetricBase(BaseModel):
    asset_id: int = Field(..., ge=1)
    plataforma: PlataformaLiteral  # ou: str

    views: Optional[int] = Field(None, ge=0)
    likes: Optional[int] = Field(None, ge=0)
    comments: Optional[int] = Field(None, ge=0)
    shares: Optional[int] = Field(None, ge=0)
    engagement: Optional[int] = Field(None, ge=0)
    reach: Optional[int] = Field(None, ge=0)

    # JSON bruto da captura (opcional)
    raw_json: Optional[dict] = None

class MetricCreate(MetricBase):
    pass

class MetricUpdate(BaseModel):
    plataforma: Optional[PlataformaLiteral] = None  # ou: Optional[str]
    views: Optional[int] = Field(None, ge=0)
    likes: Optional[int] = Field(None, ge=0)
    comments: Optional[int] = Field(None, ge=0)
    shares: Optional[int] = Field(None, ge=0)
    engagement: Optional[int] = Field(None, ge=0)
    reach: Optional[int] = Field(None, ge=0)
    raw_json: Optional[dict] = None

class MetricOut(MetricBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    capturado_em: datetime
