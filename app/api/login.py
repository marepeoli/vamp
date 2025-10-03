from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioLogin, UsuarioOut
from app.crud.usuario import autenticar_usuario
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=UsuarioOut)
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        user = autenticar_usuario(db, usuario.login, usuario.senha)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        return user
    except Exception as e:
        print("Erro no login:", e)
        raise HTTPException(status_code=500, detail=str(e))
