from sqlalchemy.orm import Session
from app.models.usuario import Usuario

def autenticar_usuario(db: Session, login: str, senha: str):
    print(f"[DEBUG] Login recebido: {login}")
    print(f"[DEBUG] Senha recebida: {senha}")
    usuario = db.query(Usuario).filter(Usuario.email == login).first()
    print(f"[DEBUG] Usuário encontrado: {usuario}")
    if usuario and usuario.senha == senha:
        print("[DEBUG] Autenticação bem-sucedida!")
        return usuario
    print("[DEBUG] Falha na autenticação!")
    return None
