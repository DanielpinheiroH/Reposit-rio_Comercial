from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon, ClassConteudo


class ConteudoEspecialCreate(AssetBaseCommon):
    tipo_asset: Literal["conteudo_especial"] = "conteudo_especial"
    plataforma: Literal["site"] = "site"
    formato: Optional[str] = "artigo"
    classificacao_conteudo_especial: ClassConteudo


class ConteudoEspecialUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["conteudo_especial"]] = None
    plataforma: Optional[Literal["site"]] = None
    formato: Optional[str] = None
    classificacao_conteudo_especial: Optional[ClassConteudo] = None


class ConteudoEspecialOut(AssetOutCommon):
    tipo_asset: Literal["conteudo_especial"]
    plataforma: Literal["site"]
    classificacao_conteudo_especial: ClassConteudo
