from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel
import sqlite3
import hashlib
from typing import List
from datetime import datetime, date, timedelta

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[  # broadened during dev to avoid CORS/host mismatches
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOGGING MIDDLEWARE: registra todas as requisições (útil para debugar 404)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"➡️ {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"⬅️ {request.method} {request.url.path} -> {response.status_code}")
    return response

# DEBUG ROUTE: lista rotas registradas para confirmar endpoints disponíveis
@app.get("/__routes")
async def list_routes():
    routes = []
    for r in app.routes:
        # Some routes are Starlette static routes and may not have .methods
        methods = list(getattr(r, "methods", []) or [])
        routes.append({"path": getattr(r, "path", str(r)), "name": getattr(r, "name", None), "methods": methods})
    return {"routes": routes}

# Modelos
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    username: str
    token: str

class UserBase(BaseModel):
    name: str
    email: str

class User(UserBase):
    id: int
    created_at: str

class EventBase(BaseModel):
    title: str
    description: str
    date: str
    location: str

class Event(EventBase):
    id: int
    created_at: str

class Recomendacao(BaseModel):
    id: int
    titulo: str
    descricao: str
    tipo: str  # "evento", "dica", "novidade"

class DiaCheckin(BaseModel):
    dia: int
    mes: str
    checkins: int

class CheckinRapido(BaseModel):
    id: int
    data: str
    hora: str
    modalidade: str
    disponivel: bool

class CheckinRequest(BaseModel):
    treino_id: int
    usuario_email: str

# Banco de dados
def get_db_connection():
    conn = sqlite3.connect('vampclubfinal.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash simples da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    
    # Tabela de usuários para login
    conn.execute('''
        CREATE TABLE IF NOT EXISTS login_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verificar se já existe o usuário admin
    admin_exists = conn.execute(
        'SELECT id FROM login_users WHERE username = ?', 
        ('admin',)
    ).fetchone()
    
    if not admin_exists:
        # Criar usuário admin padrão
        conn.execute(
            'INSERT INTO login_users (username, password) VALUES (?, ?)',
            ('admin', hash_password('admin'))
        )
        print("✅ Usuário admin criado com sucesso!")
    
    # Criar tabela usuario com as colunas corretas (apenas se não existir)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Remover criação automática de usuários - usar apenas os existentes no banco
    # Os usuários já existem: mare.oliveira@icloud.com, dayane@gmail.com, etc.
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,               -- ISO date YYYY-MM-DD
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
    conn.commit()

    # Seed inicial dos treinos (apenas se estiver vazio)
    cur = conn.execute('SELECT COUNT(1) as cnt FROM treinos').fetchone()
    if cur and cur['cnt'] == 0:
        print("⚙️ Sem treinos no DB — semeando próximos 30 dias")
        seed_treinos(conn, days=30)
    conn.close()

def seed_treinos(conn, days: int = 30):
    """Insere treinos para os próximos `days` dias seguindo padrões de horário/modalidade."""
    hoje = date.today()
    modalidades_por_dia = {
        0: ("Basquete", "Quadra A", "18:00"),  # Segunda
        1: ("Futsal", "Quadra B", "19:00"),   # Terça
        2: ("Vôlei", "Quadra A", "18:30"),    # Quarta
        3: ("Futsal", "Quadra B", "19:00"),   # Quinta
        4: ("Basquete", "Quadra A", "19:30"), # Sexta
        5: ("Futsal", "Quadra A", "09:00"),   # Sábado (exemplo)
        6: (None, None, None),                # Domingo - sem treino
    }
    vagas_default = 12

    for i in range(days):
        d = hoje + timedelta(days=i)
        wd = d.weekday()  # 0=Mon .. 6=Sun
        modal = modalidades_por_dia.get(wd)
        if not modal or modal[0] is None:
            continue
        modalidade, local, hora = modal
        conn.execute('''
            INSERT INTO treinos (data, hora, modalidade, local, vagas_total, vagas_disponiveis)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (d.isoformat(), hora, modalidade, local, vagas_default, vagas_default))
    conn.commit()
    print(f"✅ Seed de treinos criado para os próximos {days} dias")

@app.on_event("startup")
async def startup():
    init_db()
    print("🚀 FastAPI startup completo - rotas registradas")

# Rotas
@app.get("/")
async def root():
    return {"message": "VampClub API está rodando!"}

@app.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    print(f"🔍 Tentativa de login: {credentials.username}")

    conn = get_db_connection()
    
    # Buscar usuário na tabela usuario (pode ser por email ou nome)
    user = conn.execute(
        'SELECT * FROM usuario WHERE email = ? OR nome = ?',
        (credentials.username.strip(), credentials.username.strip())
    ).fetchone()
    conn.close()

    if not user:
        print(f"❌ Usuário não encontrado: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    # Verificar senha (comparar diretamente já que no banco está em texto plano)
    if credentials.password.strip() != user['senha']:
        print(f"❌ Senha incorreta para: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    print(f"✅ Login bem-sucedido: {credentials.username}")
    return LoginResponse(
        message="Login realizado com sucesso",
        username=user['nome'],
        token=f"token-{user['id']}-{datetime.now().timestamp()}"
    )

@app.get("/api/users", response_model=List[User])
async def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return [dict(user) for user in users]

@app.post("/api/users", response_model=User)
async def create_user(user: UserBase):
    conn = get_db_connection()
    try:
        # Adiciona senha padrão '123456' para novos usuários (ajuste conforme necessário)
        password = hash_password("123456")
        cursor = conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (user.name, user.email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        new_user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(new_user)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email já cadastrado")

@app.get("/api/events", response_model=List[Event])
async def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY date DESC').fetchall()
    conn.close()
    return [dict(event) for event in events]

@app.post("/api/events", response_model=Event)
async def create_event(event: EventBase):
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO events (title, description, date, location) VALUES (?, ?, ?, ?)',
        (event.title, event.description, event.date, event.location)
    )
    conn.commit()
    event_id = cursor.lastrowid
    new_event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()
    return dict(new_event)

@app.get("/api/events/{event_id}", response_model=Event)
async def get_event(event_id: int):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()
    if event is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return dict(event)

@app.delete("/api/events/{event_id}")
async def delete_event(event_id: int):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return {"message": "Evento deletado com sucesso"}

@app.get("/admin/recomendacoes")
async def get_recomendacoes():
    """Retorna recomendações para o dashboard"""
    print("📊 Endpoint /admin/recomendacoes chamado")
    recomendacoes = [
        {
            "id": 1,
            "titulo": "Treinos de Verão 2025",
            "descricao": "Prepare-se para o verão com nossos treinos intensivos de janeiro e fevereiro",
            "tipo": "evento"
        },
        {
            "id": 2,
            "titulo": "Campeonato InterVamp",
            "descricao": "Inscrições abertas para o campeonato interno de todas as modalidades",
            "tipo": "evento"
        },
        {
            "id": 3,
            "titulo": "Dica: Hidratação",
            "descricao": "Beba pelo menos 500ml de água 2 horas antes do treino para melhor performance",
            "tipo": "dica"
        }
    ]
    print(f"✅ Retornando {len(recomendacoes)} recomendações")
    return recomendacoes

# --- ADDED: aliases para evitar 404 por variações de URL do frontend ---
@app.get("/admin/recomendacoes/")
async def get_recomendacoes_trailing():
    """Alias com barra final"""
    return await get_recomendacoes()

@app.get("/api/admin/recomendacoes")
async def get_recomendacoes_api():
    """Alias sob /api/admin para clientes que usam esse prefixo"""
    return await get_recomendacoes()

@app.get("/api/admin/recomendacoes/")
async def get_recomendacoes_api_trailing():
    """Alias com barra final sob /api/admin"""
    return await get_recomendacoes()
# --- end aliases ---

@app.get("/admin/dias-checkin")
async def get_dias_checkin():
    """Retorna dados dos próximos treinos disponíveis para check-in (baseados na tabela treinos)."""
    print("📊 Endpoint /admin/dias-checkin chamado (via tabela treinos)")
    conn = get_db_connection()
    hoje = date.today()
    fim = hoje + timedelta(days=30)
    rows = conn.execute(
        'SELECT * FROM treinos WHERE data BETWEEN ? AND ? ORDER BY data ASC',
        (hoje.isoformat(), fim.isoformat())
    ).fetchall()
    conn.close()

    # Filtrar apenas sábados e pegar próximos 4 únicos
    sabados = []
    for r in rows:
        d = datetime.fromisoformat(r['data']).date()
        if d.weekday() == 5:  # sábado
            sabados.append({
                "id": r['id'],
                "dia": d.day,
                "mes": d.month,
                "ano": d.year,
                "local": r['local'],
                "horario": r['hora'],
                "modalidade": r['modalidade'],
                "vagas_disponiveis": r['vagas_disponiveis']
            })
        if len(sabados) >= 4:
            break

    print(f"✅ Retornando {len(sabados)} treinos (sábados)")
    return sabados

@app.get("/api/proximos-checkins")
async def get_proximos_checkins():
    """Retorna os próximos check-ins disponíveis baseado na tabela treinos (próximos 7 dias)."""
    print("📅 Buscando próximos check-ins disponíveis (tabela treinos)")
    conn = get_db_connection()
    hoje = date.today()
    inicio = hoje
    fim = hoje + timedelta(days=30)  # Aumentado para 30 dias para pegar os sábados de novembro
    rows = conn.execute(
        'SELECT * FROM treinos WHERE data BETWEEN ? AND ? ORDER BY data ASC, hora ASC',
        (inicio.isoformat(), fim.isoformat())
    ).fetchall()
    conn.close()

    proximos = []
    for r in rows:
        d = datetime.fromisoformat(r['data']).date()
        # Filtrar apenas sábados (como na tela de check-in)
        if d.weekday() == 5:  # sábado
            proximos.append({
                "id": r['id'],
                "data": r['data'],
                "dia_semana": "Sábado",
                "hora": r['hora'],
                "modalidade": r['modalidade'],
                "vagas_disponiveis": r['vagas_disponiveis'],
                "disponivel": bool(r['vagas_disponiveis'] > 0),
                "local": r['local']
            })
    
    print(f"✅ Retornando {len(proximos)} check-ins disponíveis (sábados)")
    return proximos

@app.post("/api/checkin-rapido")
async def fazer_checkin_rapido(checkin: CheckinRequest):
    """Realiza check-in rápido em um treino: verifica vagas, decrementa e registra checkin."""
    print(f"🔔 Tentativa de checkin rápido - Treino ID: {checkin.treino_id}, Usuário: {checkin.usuario_email}")
    conn = get_db_connection()
    try:
        # Iniciar transação explícita
        cur = conn.execute('SELECT * FROM treinos WHERE id = ?', (checkin.treino_id,))
        treino = cur.fetchone()
        if treino is None:
            raise HTTPException(status_code=404, detail="Treino não encontrado")

        if treino['vagas_disponiveis'] <= 0:
            raise HTTPException(status_code=400, detail="Não há vagas disponíveis para este treino")

        # decrementar vaga e inserir checkin
        conn.execute(
            'UPDATE treinos SET vagas_disponiveis = vagas_disponiveis - 1 WHERE id = ? AND vagas_disponiveis > 0',
            (checkin.treino_id,)
        )
        conn.execute(
            'INSERT INTO checkins (treino_id, usuario_email, timestamp) VALUES (?, ?, ?)',
            (checkin.treino_id, checkin.usuario_email, datetime.now().isoformat())
        )
        conn.commit()

        # obter vagas atualizadas
        updated = conn.execute('SELECT vagas_disponiveis FROM treinos WHERE id = ?', (checkin.treino_id,)).fetchone()
        vagas_restantes = updated['vagas_disponiveis'] if updated else 0

        print(f"✅ Check-in realizado: treino {checkin.treino_id}, vagas restantes: {vagas_restantes}")
        return {
            "message": "Check-in realizado com sucesso!",
            "treino_id": checkin.treino_id,
            "usuario": checkin.usuario_email,
            "vagas_restantes": vagas_restantes,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        conn.rollback()
        print(f"❌ Check-in falhou: {e.detail}")
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro interno no check-in rápido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar check-in")
    finally:
        conn.close()
