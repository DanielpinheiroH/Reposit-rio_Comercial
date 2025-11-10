import enum
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    Enum,
    DateTime,
    Date,
    ForeignKey,
    JSON,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from .database import Base


class TipoAssetEnum(str, enum.Enum):
    conteudo_especial = "conteudo_especial"
    live_youtube = "live_youtube"
    social_video_testemunhal = "social_video_testemunhal"
    post_instagram = "post_instagram"
    post_tiktok = "post_tiktok"
    post_kwai = "post_kwai"
    post_youtube_shorts = "post_youtube_shorts"


class PlataformaEnum(str, enum.Enum):
    site = "site"
    youtube = "youtube"
    instagram = "instagram"
    tiktok = "tiktok"
    kwai = "kwai"
    youtube_shorts = "youtube_shorts"


class ClassConteudoEnum(str, enum.Enum):
    publicidade = "Publicidade"
    nativa = "Nativa"
    artigo_opiniao = "Artigo de Opinião"
    conteudo_casa = "Conteúdo da casa"


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("url", name="uq_assets_url"),
        UniqueConstraint("external_id", "plataforma", name="uq_assets_external_platform"),
    )

    id = Column(BigInteger, primary_key=True, index=True)

    tipo_asset = Column(Enum(TipoAssetEnum, name="tipo_asset_enum"), nullable=False)
    plataforma = Column(Enum(PlataformaEnum, name="plataforma_enum"), nullable=False)
    formato = Column(String(30), nullable=True)

    titulo = Column(Text, nullable=False)
    descricao = Column(Text, nullable=True)

    url = Column(Text, nullable=False)
    external_id = Column(String(255), nullable=True)
    thumbnail_url = Column(Text, nullable=True)

    data_publicacao = Column(DateTime(timezone=True), nullable=True)
    duracao_seg = Column(Integer, nullable=True)

    classificacao_conteudo_especial = Column(
        Enum(ClassConteudoEnum, name="class_conteudo_enum"),
        nullable=True,
    )

    segmento = Column(Text, nullable=True)
    campanha = Column(Text, nullable=True)
    cliente = Column(Text, nullable=True)

    # Usando JSON para funcionar em SQLite e Postgres
    # Pydantic já trata como List[str] no schema
    tags = Column(JSON, nullable=True)

    autor_equipe = Column(Text, nullable=True)
    direitos_expira_em = Column(Date, nullable=True)

    observacoes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    metrics = relationship("Metric", back_populates="asset", cascade="all, delete-orphan")
    collections = relationship(
        "Collection",
        secondary="collection_items",
        back_populates="assets",
    )
    testemunhos = relationship(
        "PessoaTestemunho",
        back_populates="asset",
        cascade="all, delete-orphan",
    )
    attachments = relationship(
        "Attachment",
        back_populates="asset",
        cascade="all, delete-orphan",
    )


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(BigInteger, primary_key=True, index=True)
    asset_id = Column(BigInteger, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    plataforma = Column(Enum(PlataformaEnum, name="plataforma_enum"), nullable=False)

    capturado_em = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    views = Column(BigInteger, nullable=True)
    likes = Column(BigInteger, nullable=True)
    comments = Column(BigInteger, nullable=True)
    shares = Column(BigInteger, nullable=True)
    engagement = Column(Integer, nullable=True)
    reach = Column(BigInteger, nullable=True)

    raw_json = Column(JSON, nullable=True)

    asset = relationship("Asset", back_populates="metrics")


class Collection(Base):
    __tablename__ = "collections"

    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    assets = relationship(
        "Asset",
        secondary="collection_items",
        back_populates="collections",
    )


class CollectionItem(Base):
    __tablename__ = "collection_items"

    collection_id = Column(
        BigInteger,
        ForeignKey("collections.id", ondelete="CASCADE"),
        primary_key=True,
    )
    asset_id = Column(
        BigInteger,
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(BigInteger, primary_key=True, index=True)
    asset_id = Column(BigInteger, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)

    nome_arquivo = Column(Text, nullable=False)
    tipo_mime = Column(String(255), nullable=True)
    url_arquivo = Column(Text, nullable=False)
    tamanho_bytes = Column(BigInteger, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    asset = relationship("Asset", back_populates="attachments")


class PessoaTestemunho(Base):
    __tablename__ = "pessoas_testemunho"

    id = Column(BigInteger, primary_key=True, index=True)
    asset_id = Column(BigInteger, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)

    nome = Column(Text, nullable=False)
    cargo = Column(Text, nullable=True)
    empresa = Column(Text, nullable=True)
    contato = Column(Text, nullable=True)

    asset = relationship("Asset", back_populates="testemunhos")
