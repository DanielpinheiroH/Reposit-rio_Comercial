from typing import Optional, Literal
from .asset_common import AssetBaseCommon, AssetOutCommon


class LiveYoutubeCreate(AssetBaseCommon):
    tipo_asset: Literal["live_youtube"] = "live_youtube"
    plataforma: Literal["youtube"] = "youtube"
    formato: Optional[str] = "live"


class LiveYoutubeUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["live_youtube"]] = None
    plataforma: Optional[Literal["youtube"]] = None
    formato: Optional[str] = None


class LiveYoutubeOut(AssetOutCommon):
    tipo_asset: Literal["live_youtube"]
    plataforma: Literal["youtube"]
