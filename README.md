# VampClub App

Sistema de gerenciamento de treinos e eventos esportivos com dashboard administrativo.

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web Python
- **SQLite** - Banco de dados
- **Pydantic** - Validação de dados

### Frontend
- **React** - Biblioteca JavaScript
- **Tailwind CSS** - Framework de estilização
- **React Icons** - Ícones
- **Axios** - Cliente HTTP

## 📋 Funcionalidades

- ✅ Sistema de login/autenticação
- ✅ Dashboard administrativo
- ✅ Gerenciamento de eventos
- ✅ Sistema de check-in para treinos
- ✅ Calendário de atividades
- ✅ Estatísticas e recomendações

## 🛠️ Como executar

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- npm ou yarn

### Backend (FastAPI)

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/vampclub-app.git
cd vampclub-app
```

2. Crie um ambiente virtual Python:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o servidor:
```bash
uvicorn main:app --reload
```

O backend estará rodando em `http://localhost:8000`

### Frontend (React)

1. Navegue para a pasta do frontend:
```bash
cd frontend-app
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o frontend:
```bash
npm start
```

O frontend estará rodando em `http://localhost:3000`

## 📊 API Endpoints

### Autenticação
- `POST /login` - Login de usuário

### Eventos
- `GET /api/events` - Listar eventos
- `POST /api/events` - Criar evento
- `DELETE /api/events/{id}` - Deletar evento

### Check-ins
- `GET /api/proximos-checkins` - Próximos treinos disponíveis
- `POST /api/checkin-rapido` - Realizar check-in

### Dashboard
- `GET /admin/recomendacoes` - Recomendações do dashboard
- `GET /admin/dias-checkin` - Estatísticas de check-in

## 🗄️ Banco de Dados

O projeto usa SQLite com as seguintes tabelas:
- `usuario` - Dados dos usuários
- `events` - Eventos do clube
- `treinos` - Sessões de treino
- `checkins` - Registros de check-in

## 📝 Licença

Este projeto está sob a licença MIT.