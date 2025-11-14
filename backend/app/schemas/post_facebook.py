from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, AnyHttpUrl, ConfigDict


class PostFacebookBase(BaseModel):
    titulo: str
    url: AnyHttpUrl
    descricao: Optional[str] = None
    thumbnail_url: Optional[AnyHttpUrl] = None

    data_publicacao: Optional[datetime] = None
    campanha: Optional[str] = None
    cliente: Optional[str] = None
    segmento: Optional[str] = None
    tags: Optional[List[str]] = None
    observacoes: Optional[str] = None


class PostFacebookCreate(PostFacebookBase):
    pass


class PostFacebookUpdate(BaseModel):
    titulo: Optional[str] = None
    url: Optional[AnyHttpUrl] = None
    descricao: Optional[str] = None
    thumbnail_url: Optional[AnyHttpUrl] = None

    data_publicacao: Optional[datetime] = None
    campanha: Optional[str] = None
    cliente: Optional[str] = None
    segmento: Optional[str] = None
    tags: Optional[List[str]] = None
    observacoes: Optional[str] = None


class PostFacebookOut(PostFacebookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # sempre fixos neste router:
    # tipo_asset = "post_facebook"
    # plataforma = "facebook"
    # formato = "feed"
