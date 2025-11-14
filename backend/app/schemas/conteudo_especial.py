from datetime import datetime, date
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

# Slugs escolhidos por você
ConteudoSiteFormato = Literal[
    "expressao_de_opiniao_digital",
    "publicidade_nativa",
    "publieditorial",
    "manchete",
    "sub_manchete",
]

# Mantendo compatível com o Enum do models
ClassConteudo = Literal[
    "Publicidade",
    "Nativa",
    "Artigo de Opinião",
    "Conteúdo da casa",
]


class ConteudoEspecialBase(BaseModel):
    titulo: str = Field(..., max_length=500)
    url: HttpUrl
    # ↓ obrigamos formato aqui (antes era opcional)
    formato: ConteudoSiteFormato

    descricao: Optional[str] = None
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

    classificacao_conteudo_especial: Optional[ClassConteudo] = None


class ConteudoEspecialCreate(ConteudoEspecialBase):
    pass


class ConteudoEspecialUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=500)
    url: Optional[HttpUrl] = None
    formato: Optional[ConteudoSiteFormato] = None

    descricao: Optional[str] = None
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

    classificacao_conteudo_especial: Optional[ClassConteudo] = None


class ConteudoEspecialOut(ConteudoEspecialBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo_asset: str
    plataforma: str
    created_at: datetime
    updated_at: datetime
