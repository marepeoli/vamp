from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, Body
import sqlite3
import hashlib
from typing import Dict, Any
from datetime import datetime

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOGGING MIDDLEWARE
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"➡️ {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"⬅️ {request.method} {request.url.path} -> {response.status_code}")
    return response

# Banco de dados (mesmo código do arquivo original)
def get_db_connection():
    conn = sqlite3.connect('vampclubfinal.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    
    # Criar tabelas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            modalidade TEXT NOT NULL,
            local TEXT NOT NULL,
            vagas_total INTEGER NOT NULL,
            vagas_disponiveis INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treino_id INTEGER NOT NULL,
            usuario_email TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(treino_id) REFERENCES treinos(id)
        )
    ''')
    
    conn.commit()inos reais se não existirem
    conn.close()
        ("2025-11-15", "09:00", "Futsal", "Sest Senat", 8),
@app.on_event("startup")09:00", "Futsal", "Sest Senat", 8),
async def startup():", "09:00", "Futsal", "Sest Senat", 8),
    init_db()5-12-06", "09:00", "Futsal", "Sest Senat", 8),
    print("🚀 FastAPI startup completo - modo simples") 8),
        ("2025-12-20", "09:00", "Futsal", "Sest Senat", 8),
# Rotas simplificadas (sem Pydantic models complexos)
@app.get("/") hora, modalidade, local, vagas in treinos:
async def root():conn.execute(
    return {"message": "VampClub API está rodando! (Modo Simples)"} modalidade = ? AND local = ?",
            (data, hora, modalidade, local)
@app.post("/login"))
async def login(credentials: Dict[str, Any]):
    print(f"🔍 Tentativa de login: {credentials.get('username')}")
                "INSERT INTO treinos (data, hora, modalidade, local, vagas_total, vagas_disponiveis) VALUES (?, ?, ?, ?, ?, ?)",
    conn = get_db_connection()odalidade, local, vagas, vagas)
    # Busca apenas pelo email
    user = conn.execute(
        'SELECT * FROM usuario WHERE email = ?',
        (credentials.get('username', '').strip(),)
    ).fetchone()
    conn.close()tartup")
async def startup():
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    # Comparação direta da senha (sem hash)complexos)
    if credentials.get('password', '').strip() != user['senha']:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    return {"message": "VampClub API está rodando! (Modo Simples)"}
    return {
        "message": "Login realizado com sucesso",
        "username": user['email'],str, Any]):
        "token": f"token-{user['id']}-{datetime.now().timestamp()}"
    }
    conn = get_db_connection()
@app.get("/admin/recomendacoes")
async def get_recomendacoes():
    return [ECT * FROM usuario WHERE email = ?',
        {credentials.get('username', '').strip(),)
            "id": 1,
            "titulo": "Próximo Intervamp XII",
            "descricao": "Lorem ipsum dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
            "tipo": "evento",
            "imagem": "/eventos1.png"de=401, detail="Usuário ou senha inválidos")
        },
        {paração direta da senha (sem hash)
            "id": 2,et('password', '').strip() != user['senha']:
            "titulo": "Intervamp XI",de=401, detail="Usuário ou senha inválidos")
            "descricao": "Lorem ipsum dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
            "tipo": "evento",
            "imagem": "/XIintervamp.png"sucesso",
        },sername": user['email'],
        {token": f"token-{user['id']}-{datetime.now().timestamp()}"
            "id": 3,
            "titulo": "Intervamp VIII",
            "descricao": "Lorem ipsum dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
            "tipo": "evento",:
            "imagem": "/viiiintervamp.png"
        },
        {   "id": 1,
            "id": 4,: "Próximo Intervamp XII",
            "titulo": "Outros Intervamps",r sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
            "descricao": "Lorem ipsum dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
            "tipo": "evento",os1.png"
            "imagem": "/intervampx.png"
        }
    ]       "id": 2,
            "titulo": "Intervamp XI",
@app.get("/api/proximos-checkins")sum dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
async def get_proximos_checkins():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, data, hora, modalidade, local, vagas_disponiveis FROM treinos ORDER BY data ASC"
    ).fetchall()
    conn.close()VIII",
    dias_semana = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]um dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
    result = [],
    for row in rows:mp.png"
        data_obj = datetime.strptime(row["data"], "%Y-%m-%d")
        dia_semana = dias_semana[data_obj.weekday()]
        result.append({
            "id": row["id"],  "titulo": "Outros Intervamps",
            "data": row["data"],   "descricao": "Lorem ipsum dolor sit amet consectetur. Magnis pellentesque felis ullamcorper imperdiet.",
            "dia_semana": dia_semana,"evento",
            "hora": row["hora"],x.png"
            "modalidade": row["modalidade"],
            "vagas_disponiveis": row["vagas_disponiveis"],
            "disponivel": row["vagas_disponiveis"] > 0,
            "local": row["local"]
        })():
    return results de novembro e dezembro de 2025
 [
from fastapi import Body

@app.post("/api/checkin-rapido")
async def checkin_rapido(payload: Dict[str, Any] = Body(...)):
    treino_id = payload.get("treino_id")
    usuario_email = payload.get("usuario_email")
    if not treino_id or not usuario_email:
        raise HTTPException(status_code=400, detail="treino_id e usuario_email são obrigatórios")

    conn = get_db_connection()
    # Verifica se já existe check-in para esse treino e usuário
    existe = conn.execute(
        "SELECT id FROM checkins WHERE treino_id = ? AND usuario_email = ?",
        (treino_id, usuario_email)
    ).fetchone()
    if existe:
        conn.close()
        raise HTTPException(status_code=409, detail="Check-in já realizado para este treino")

    # Atualiza vagas disponíveis
    treino = conn.execute(
        "SELECT vagas_disponiveis FROM treinos WHERE id = ?",
        (treino_id,)
    ).fetchone()
    if treino and treino["vagas_disponiveis"] <= 0:
        conn.close()
        raise HTTPException(status_code=400, detail="Não há vagas disponíveis para este treino")

    # Registra o check-in
    conn.execute(
        "INSERT INTO checkins (treino_id, usuario_email, timestamp) VALUES (?, ?, ?)",
        (treino_id, usuario_email, datetime.now().isoformat())
    )
    # Diminui uma vaga
    conn.execute(
        "UPDATE treinos SET vagas_disponiveis = vagas_disponiveis - 1 WHERE id = ?",
        (treino_id,)
    )
    conn.commit()
    conn.close(),
    return {"message": "Check-in realizado com sucesso"}   {
            "id": 5,
if __name__ == "__main__":5-12-13",
    import uvicorn            "dia_semana": "Sábado",
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        raise HTTPException(status_code=400, detail="Não há vagas disponíveis para este treino")

    # Registra o check-in
    conn.execute(
        "INSERT INTO checkins (treino_id, usuario_email, timestamp) VALUES (?, ?, ?)",
        (treino_id, usuario_email, datetime.now().isoformat())
    )
    # Diminui uma vaga
    conn.execute(
        "UPDATE treinos SET vagas_disponiveis = vagas_disponiveis - 1 WHERE id = ?",
        (treino_id,)
    )
    conn.commit()
    conn.close()
    return {"message": "Check-in realizado com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
