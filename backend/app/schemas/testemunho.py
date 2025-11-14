from typing import Optional
from pydantic import BaseModel, ConfigDict


class PessoaTestemunhoBase(BaseModel):
    nome: str
    cargo: Optional[str] = None
    empresa: Optional[str] = None
    contato: Optional[str] = None


class PessoaTestemunhoCreate(PessoaTestemunhoBase):
    pass


class PessoaTestemunhoOut(PessoaTestemunhoBase):
    id: int
    asset_id: int

    model_config = ConfigDict(from_attributes=True)
