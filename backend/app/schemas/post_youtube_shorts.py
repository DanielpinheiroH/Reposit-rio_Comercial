from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon


class YoutubeShortsCreate(AssetBaseCommon):
    tipo_asset: Literal["post_youtube_shorts"] = "post_youtube_shorts"
    plataforma: Literal["youtube_shorts"] = "youtube_shorts"
    formato: Optional[str] = "shorts"


class YoutubeShortsUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["post_youtube_shorts"]] = None
    plataforma: Optional[Literal["youtube_shorts"]] = None
    formato: Optional[str] = None


class YoutubeShortsOut(AssetOutCommon):
    tipo_asset: Literal["post_youtube_shorts"]
    plataforma: Literal["youtube_shorts"]
