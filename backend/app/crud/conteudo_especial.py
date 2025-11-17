# backend/app/crud/conteudo_especial.py

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models
from ..models import TipoAssetEnum, PlataformaEnum
from ..schemas.conteudo_especial import (
    ConteudoEspecialCreate,
    ConteudoEspecialUpdate,
    ConteudoEspecialOut,
)
from .assets_base import (
    create_asset,
    list_assets,
    get_asset,
    update_asset,
    delete_asset,
)

# Slugs aceitos (batendo com o schema e o router)
FORMATS_ALLOWED = {
    "expressao_de_opiniao_digital",
    "publicidade_nativa",
    "publieditorial",
    "manchete",
    "sub_manchete",
}


def create_conteudo_especial(
    db: Session,
    payload: ConteudoEspecialCreate,
) -> models.Asset:
    """
    Cria um Conteúdo Especial:
    - tipo_asset = conteudo_especial
    - plataforma = site
    """
    data = payload.model_dump()

    # Aqui assumimos que o router já validou o formato.
    data.update(
        {
            "tipo_asset": TipoAssetEnum.conteudo_especial,
            "plataforma": PlataformaEnum.site,
        }
    )
    asset = create_asset(db, data)
    return asset


def list_conteudo_especial(
    db: Session,
    formato: Optional[str] = None,
    campanha: Optional[str] = None,
    cliente: Optional[str] = None,
    search: Optional[str] = None,
    classificacao: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[ConteudoEspecialOut]:
    """
    Lista Conteúdos Especiais com filtros opcionais:
    - formato (slug)
    - campanha
    - cliente
    - search (título/descrição/campanha/cliente)
    - classificacao (opcional, se usado em alguma lógica interna)
    """
    items = list_assets(
        db=db,
        tipo_asset=TipoAssetEnum.conteudo_especial.value,
        plataforma=PlataformaEnum.site.value,
        formato=formato,
        campanha=campanha,
        cliente=cliente,
        search=search,
        skip=skip,
        limit=limit,
    )

    # Filtro adicional por classificacao_conteudo_especial, se fornecido
    if classificacao:
        items = [
            a
            for a in items
            if getattr(a, "classificacao_conteudo_especial", None)
            and str(a.classificacao_conteudo_especial.value)
            == classificacao
        ]

    return items


def get_conteudo_especial(
    db: Session,
    asset_id: int,
) -> Optional[models.Asset]:
    """
    Busca um Conteúdo Especial garantindo o tipo correto.
    Retorna None se não for conteudo_especial.
    """
    obj = get_asset(db, asset_id)
    if not obj or obj.tipo_asset != TipoAssetEnum.conteudo_especial:
        return None
    return obj


def update_conteudo_especial(
    db: Session,
    asset_id: int,
    payload: ConteudoEspecialUpdate,
) -> Optional[models.Asset]:
    """
    Atualiza um Conteúdo Especial.
    Não permite trocar tipo_asset/plataforma.
    """
    obj = get_asset(db, asset_id)
    if not obj or obj.tipo_asset != TipoAssetEnum.conteudo_especial:
        return None

    data = payload.model_dump(exclude_unset=True)

    # Proteção extra: não deixa sobrescrever tipo/plataforma
    data.pop("tipo_asset", None)
    data.pop("plataforma", None)

    # Mantém fixo plataforma=site
    data["plataforma"] = PlataformaEnum.site

    updated = update_asset(db, obj, data)
    return updated


def delete_conteudo_especial(
    db: Session,
    asset_id: int,
) -> bool:
    """
    Deleta um Conteúdo Especial.
    Retorna:
    - True se deletou
    - False se não encontrou / tipo errado.
    """
    obj = get_asset(db, asset_id)
    if not obj or obj.tipo_asset != TipoAssetEnum.conteudo_especial:
        return False

    delete_asset(db, asset_id)
    return True
