from pydantic import BaseModel

class UsuarioLogin(BaseModel):
    login: str
    senha: str

class UsuarioOut(BaseModel):
    id: int
    email: str
    perfil_id: int
    class Config:
        orm_mode = True
