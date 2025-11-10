from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon


class InstagramPostCreate(AssetBaseCommon):
    tipo_asset: Literal["post_instagram"] = "post_instagram"
    plataforma: Literal["instagram"] = "instagram"
    formato: Literal["feed", "reels"]


class InstagramPostUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["post_instagram"]] = None
    plataforma: Optional[Literal["instagram"]] = None
    formato: Optional[Literal["feed", "reels"]] = None


class InstagramPostOut(AssetOutCommon):
    tipo_asset: Literal["post_instagram"]
    plataforma: Literal["instagram"]
