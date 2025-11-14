from datetime import datetime, date
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


YouTubeTalkFormato = Literal["big_talk", "one_talk", "little_talk"]


class YouTubeTalkBase(BaseModel):
    # Campos comuns
    titulo: str = Field(..., max_length=500)
    descricao: Optional[str] = None
    url: HttpUrl
    external_id: Optional[str] = Field(None, max_length=255)
    thumbnail_url: Optional[HttpUrl] = None

    data_publicacao: Optional[datetime] = None
    duracao_seg: Optional[int] = Field(None, ge=0)

    # Organização
    segmento: Optional[str] = None
    campanha: Optional[str] = None
    cliente: Optional[str] = None  # "Anunciante"
    tags: Optional[List[str]] = None

    # Autoria / direitos / observações
    autor_equipe: Optional[str] = None
    direitos_expira_em: Optional[date] = None
    observacoes: Optional[str] = None

    # Específico
    formato: Optional[YouTubeTalkFormato] = None  # big_talk | one_talk | little_talk


class YouTubeTalkCreate(YouTubeTalkBase):
    pass


class YouTubeTalkUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=500)
    descricao: Optional[str] = None
    url: Optional[HttpUrl] = None
    external_id: Optional[str] = Field(None, max_length=255)
    thumbnail_url: Optional[HttpUrl] = None

    data_publicacao: Optional[datetime] = None
    duracao_seg: Optional[int] = Field(None, ge=0)

    segmento: Optional[str] = None
    campanha: Optional[str] = None
    cliente: Optional[str] = None
    tags: Optional[List[str]] = None

    autor_equipe: Optional[str] = None
    direitos_expira_em: Optional[date] = None
    observacoes: Optional[str] = None

    formato: Optional[YouTubeTalkFormato] = None


class YouTubeTalkOut(YouTubeTalkBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo_asset: str
    plataforma: str
    created_at: datetime
    updated_at: datetime
