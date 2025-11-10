from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon


class KwaiPostCreate(AssetBaseCommon):
    tipo_asset: Literal["post_kwai"] = "post_kwai"
    plataforma: Literal["kwai"] = "kwai"
    formato: Optional[str] = "video"


class KwaiPostUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["post_kwai"]] = None
    plataforma: Optional[Literal["kwai"]] = None
    formato: Optional[str] = None


class KwaiPostOut(AssetOutCommon):
    tipo_asset: Literal["post_kwai"]
    plataforma: Literal["kwai"]
