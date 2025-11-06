from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon


class SocialTestemunhalCreate(AssetBaseCommon):
    tipo_asset: Literal["social_video_testemunhal"] = "social_video_testemunhal"
    plataforma: Literal["instagram", "tiktok"]
    formato: Optional[str] = "reels"


class SocialTestemunhalUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["social_video_testemunhal"]] = None
    plataforma: Optional[Literal["instagram", "tiktok"]] = None
    formato: Optional[str] = None


class SocialTestemunhalOut(AssetOutCommon):
    tipo_asset: Literal["social_video_testemunhal"]
