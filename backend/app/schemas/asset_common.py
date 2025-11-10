from datetime import datetime, date
from typing import List, Optional, Literal
from pydantic import BaseModel, AnyHttpUrl, field_validator


TipoAsset = Literal[
    "conteudo_especial",
    "live_youtube",
    "social_video_testemunhal",
    "post_instagram",
    "post_tiktok",
    "post_kwai",
    "post_youtube_shorts",
]

Plataforma = Literal[
    "site",
    "youtube",
    "instagram",
    "tiktok",
    "kwai",
    "youtube_shorts",
]

ClassConteudo = Literal[
    "Publicidade",
    "Nativa",
    "Artigo de Opinião",
    "Conteúdo da casa",
]


class AssetBaseCommon(BaseModel):
    titulo: str
    descricao: Optional[str] = None

    url: AnyHttpUrl
    external_id: Optional[str] = None
    thumbnail_url: Optional[AnyHttpUrl] = None

    data_publicacao: Optional[datetime] = None
    duracao_seg: Optional[int] = None

    segmento: Optional[str] = None
    campanha: Optional[str] = None
    cliente: Optional[str] = None

    tags: Optional[List[str]] = None

    autor_equipe: Optional[str] = None
    direitos_expira_em: Optional[date] = None

    observacoes: Optional[str] = None

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return v

    class Config:
        from_attributes = True


class AssetOutCommon(AssetBaseCommon):
    id: int
    tipo_asset: str
    plataforma: str
    formato: Optional[str] = None
    classificacao_conteudo_especial: Optional[ClassConteudo] = None
    created_at: datetime
    updated_at: datetime
