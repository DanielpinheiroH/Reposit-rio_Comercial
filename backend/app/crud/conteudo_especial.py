from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .assets_base import create_asset, list_assets


def create_conteudo_especial(db: Session, data: schemas.ConteudoEspecialCreate) -> models.Asset:
    payload = data.model_dump()
    payload["tipo_asset"] = models.TipoAssetEnum.conteudo_especial
    payload["plataforma"] = models.PlataformaEnum.site
    return create_asset(db, payload)


def list_conteudo_especial(
    db: Session,
    classificacao: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Asset]:
    items = list_assets(
        db,
        tipo_asset=models.TipoAssetEnum.conteudo_especial,
        plataforma=models.PlataformaEnum.site,
        skip=skip,
        limit=limit,
        search=search,
    )
    if classificacao:
        items = [
            a
            for a in items
            if a.classificacao_conteudo_especial
            and a.classificacao_conteudo_especial.value == classificacao
        ]
    return items
