from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon


class TikTokPostCreate(AssetBaseCommon):
    tipo_asset: Literal["post_tiktok"] = "post_tiktok"
    plataforma: Literal["tiktok"] = "tiktok"
    formato: Optional[str] = "video"


class TikTokPostUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["post_tiktok"]] = None
    plataforma: Optional[Literal["tiktok"]] = None
    formato: Optional[str] = None


class TikTokPostOut(AssetOutCommon):
    tipo_asset: Literal["post_tiktok"]
    plataforma: Literal["tiktok"]
