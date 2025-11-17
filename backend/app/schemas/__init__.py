# backend/app/schemas/__init__.py

# -------------------------
# Comuns / enums
# -------------------------
from .asset_common import (
    TipoAsset,
    Plataforma,
    ClassConteudo,
    AssetBaseCommon,
    AssetOutCommon,
)

# -------------------------
# Conteúdo especial (site)
# -------------------------
from .conteudo_especial import (
    ConteudoEspecialBase,
    ConteudoEspecialCreate,
    ConteudoEspecialUpdate,
    ConteudoEspecialOut,
)

# -------------------------
# Live / YouTube (Talks antigos)
# -------------------------
from .live_youtube import (
    LiveYouTubeCreate,
    LiveYouTubeUpdate,
    LiveYouTubeOut,
)

# Aliases para compatibilidade com código legado
LiveYoutubeCreate = LiveYouTubeCreate
LiveYoutubeUpdate = LiveYouTubeUpdate
LiveYoutubeOut = LiveYouTubeOut

# -------------------------
# YouTube Talk (novo schema dedicado)
# -------------------------
from .youtube_talk import (
    YouTubeTalkBase,
    YouTubeTalkCreate,
    YouTubeTalkUpdate,
    YouTubeTalkOut,
)

# -------------------------
# Social vídeo testemunhal
# -------------------------
from .social_testemunhal import (
    SocialTestemunhalCreate,
    SocialTestemunhalUpdate,
    SocialTestemunhalOut,
)

# -------------------------
# Instagram
# -------------------------
from .post_instagram import (
    PostInstagramBase,
    PostInstagramCreate,
    PostInstagramUpdate,
    PostInstagramOut,
)

# Aliases para compatibilidade com CRUD antigo
InstagramPostCreate = PostInstagramCreate
InstagramPostUpdate = PostInstagramUpdate
InstagramPostOut = PostInstagramOut

# -------------------------
# TikTok
# -------------------------
from .post_tiktok import (
    PostTikTokBase,
    PostTikTokCreate,
    PostTikTokUpdate,
    PostTikTokOut,
)

# Aliases para compatibilidade com CRUD antigo
TikTokPostCreate = PostTikTokCreate
TikTokPostUpdate = PostTikTokUpdate
TikTokPostOut = PostTikTokOut

# -------------------------
# Kwai
# -------------------------
from .post_kwai import (
    PostKwaiBase,
    PostKwaiCreate,
    PostKwaiUpdate,
    PostKwaiOut,
)

# Aliases para compatibilidade com CRUD antigo
KwaiPostCreate = PostKwaiCreate
KwaiPostUpdate = PostKwaiUpdate
KwaiPostOut = PostKwaiOut

# -------------------------
# YouTube Shorts
# -------------------------
from .post_youtube_shorts import (
    PostYouTubeShortsBase,
    PostYouTubeShortsCreate,
    PostYouTubeShortsUpdate,
    PostYouTubeShortsOut,
)

# Aliases para compatibilidade com CRUD antigo
YoutubeShortsCreate = PostYouTubeShortsCreate
YoutubeShortsUpdate = PostYouTubeShortsUpdate
YoutubeShortsOut = PostYouTubeShortsOut

# -------------------------
# Facebook Feed
# -------------------------
from .post_facebook import (
    PostFacebookBase,
    PostFacebookCreate,
    PostFacebookUpdate,
    PostFacebookOut,
)

# -------------------------
# Métricas
# -------------------------
from .metrics import (
    MetricBase,
    MetricCreate,
    MetricUpdate,
    MetricOut,
)

# -------------------------
# Coleções
# -------------------------
from .collections import (
    CollectionBase,
    CollectionCreate,
    CollectionOut,
    CollectionItemAdd,
    CollectionWithAssets,
)

# -------------------------
# Pessoas de Testemunho (metadados de quem deu depoimento)
# -------------------------
from .testemunho import (
    PessoaTestemunhoCreate,
    PessoaTestemunhoOut,
)
