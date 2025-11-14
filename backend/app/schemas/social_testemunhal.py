from typing import Optional, Literal
from pydantic import field_validator, ConfigDict
from .asset_common import AssetBaseCommon, AssetOutCommon


# Plataforma permitida e formato fixo ("reels") para o Testemunhal
_PlataformaTestemunhal = Literal["instagram", "tiktok"]
_FormatoTestemunhal = Literal["reels"]


class SocialTestemunhalCreate(AssetBaseCommon):
    tipo_asset: Literal["social_video_testemunhal"] = "social_video_testemunhal"
    plataforma: _PlataformaTestemunhal
    formato: _FormatoTestemunhal = "reels"  # fixo

    # Validamos duração se vier (esperado 30" ou 60")
    @field_validator("duracao_seg")
    @classmethod
    def validate_duracao(cls, v):
        if v is None:
            return v
        if v not in (30, 60):
            raise ValueError("duracao_seg deve ser 30 ou 60 segundos para testemunhal.")
        return v

    model_config = ConfigDict(from_attributes=True)


class SocialTestemunhalUpdate(AssetBaseCommon):
    tipo_asset: Optional[Literal["social_video_testemunhal"]] = None
    plataforma: Optional[_PlataformaTestemunhal] = None
    formato: Optional[_FormatoTestemunhal] = None  # se vier, só "reels"

    @field_validator("duracao_seg")
    @classmethod
    def validate_duracao(cls, v):
        if v is None:
            return v
        if v not in (30, 60):
            raise ValueError("duracao_seg deve ser 30 ou 60 segundos para testemunhal.")
        return v

    model_config = ConfigDict(from_attributes=True)


class SocialTestemunhalOut(AssetOutCommon):
    tipo_asset: Literal["social_video_testemunhal"]
    plataforma: _PlataformaTestemunhal
    formato: _FormatoTestemunhal
