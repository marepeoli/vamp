from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

# CORS para permitir o frontend em localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    login: str
    senha: str

def cria_db_se_nao_existe(db_path, sql_path):
    if os.path.exists(db_path):
        return True
    if not os.path.exists(sql_path):
        return False
    try:
        conn = sqlite3.connect(db_path)
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        conn.close()
        print(f"Banco criado a partir de {sql_path}")
        return True
    except Exception as e:
        print(f"Erro ao criar DB a partir do SQL: {e}")
        return False

def verifica_usuario(login, senha):
    base_dir = os.path.dirname(__file__)
    db_file = os.path.join(base_dir, "vampclubfinal.db")
    sql_file = os.path.join(base_dir, "vampclubfinal.db")

    # tentar criar .db a partir de .sql se necessário
    if not os.path.exists(db_file):
        if not cria_db_se_nao_existe(db_file, sql_file):
            print("Arquivo do banco NÃO encontrado e .sql ausente ou falha na criação.")
            return False

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuario WHERE email=? AND senha=?", (login, senha))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except Exception as e:
        print(f"Erro ao acessar o banco: {e}")
        return False

@app.post("/login")
async def login(req: LoginRequest):
    if verifica_usuario(req.login, req.senha):
        return {"msg": "Login realizado com sucesso!"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.get("/ping")
def ping():
    return {"msg": "pong"}

@app.get("/test-login")
def test_login(login: str, senha: str):
    if verifica_usuario(login, senha):
        return {"msg": "Login realizado com sucesso!"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")
def test_login(login: str, senha: str):
    print(f"Testando login GET com: {login} {senha}")
    if verifica_usuario(login, senha):
        print("Login GET realizado com sucesso!")
        return {"msg": "Login realizado com sucesso!"}
    print("Credenciais inválidas (GET)")
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db_connection():
    # Use o caminho correto do banco, sem .sql no final se for SQLite
    conn = sqlite3.connect("vampclubfinal.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/atleta/by_email/{email}")
def get_atleta_by_email(email: str):
    conn = get_db_connection()
    usuario = conn.execute("SELECT id FROM usuario WHERE email = ?", (email,)).fetchone()
    if not usuario:
        conn.close()
        return {"nome": ""}
    atleta = conn.execute("SELECT nome FROM atleta WHERE usuario_id = ?", (usuario["id"],)).fetchone()
    conn.close()
    if atleta and atleta["nome"]:
        return {"nome": atleta["nome"]}
    return {"nome": ""}
        if atleta:
            return dict(atleta)
        return {"erro": "Atleta não encontrado"}
    except Exception as e:
        print("Erro no endpoint:", str(e))
        conn.close()
        return {"erro": str(e)}
