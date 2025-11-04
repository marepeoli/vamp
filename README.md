# VampClub - Sistema de Gestão Esportiva

## 🚀 Como Executar

### Backend (FastAPI)

1. Ativar ambiente virtual:
```bash
venv\Scripts\activate
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Iniciar o servidor:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)

1. Instalar dependências:
```bash
cd frontend-app
npm install
```

2. Iniciar o servidor:
```bash
npm start
```

## 🔐 Login

**Usuário padrão:**
- Username: `admin`
- Password: `admin`

## 📝 Criar Novos Usuários

Execute o script:
```bash
python create_user.py
```

Ou edite o arquivo para adicionar mais usuários.

## 🌐 URLs

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔐 Login
- **Usuário:** admin
- **Senha:** admin

## 🔧 Problemas Conhecidos e Soluções

### ❌ Erro 422 no Login
**Causa:** Backend não está recebendo dados JSON corretamente  
**Solução:** Já corrigido! Certifique-se de reiniciar o backend:
```bash
# Ctrl+C no terminal do backend
uvicorn main:app --reload
```

### ⚠️ Erro: SVG width negative
**Causa:** Algum componente SVG está renderizando antes dos dados carregarem  
**Solução:** No código React, adicione verificação antes de renderizar SVGs:
```javascript
{data && data.length > 0 && (
  <svg width={width} height={height}>
    {/* seu código SVG */}
  </svg>
)}
```

### ℹ️ Warnings do React Router
**Causa:** Avisos sobre futuras mudanças no React Router v7  
**Solução:** São apenas avisos, não afetam o funcionamento. Você pode ignorar por enquanto.

## 📊 Testando o Backend Manualmente

### 1. Health Check
```bash
curl http://localhost:8000
# Resposta: {"message":"VampClub API está rodando!"}
```

### 2. Testar Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin\"}"
```

### 3. Verificar Documentação
Acesse: http://localhost:8000/docs

## 🎯 Checklist de Verificação

- [ ] Backend rodando em http://localhost:8000
- [ ] Endpoint `/login` funcionando (testar em /docs)
- [ ] Frontend rodando em http://localhost:3000
- [ ] Login com admin/admin funcionando
- [ ] Console do navegador sem erros 422

## 📝 Estrutura da API

### POST /login
```json
Request:
{
  "username": "admin",
  "password": "admin"
}

Response:
{
  "message": "Login realizado com sucesso",
  "username": "admin",
  "token": "fake-token-123"
}
```

### GET /api/users
Retorna lista de usuários cadastrados

### POST /api/users
Cria novo usuário

### GET /api/events
Retorna lista de eventos

### POST /api/events
Cria novo evento

## 🆘 Solução de Problemas

### Backend não inicia
```bash
# Reinstalar dependências
pip install --only-binary=:all: --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org fastapi uvicorn pydantic python-multipart
```

### Frontend não conecta ao Backend
1. Verifique se o backend está rodando em http://localhost:8000
2. Verifique o console do navegador (F12)
3. Confirme que `proxy` está configurado no package.json do frontend

### Erro CORS
O CORS já está configurado. Se ainda houver problema:
```python
# No main.py, linha 12-17, verifique:
allow_origins=["http://localhost:3000"],  # Deve estar exatamente assim
```

## 📞 Logs Úteis

### Ver logs do backend
Os logs aparecem no terminal onde você executou `uvicorn main:app --reload`

### Ver logs do frontend
Abra o Console do Navegador (F12) → aba Console

## ✅ Validação Final

Execute este teste:
1. Backend rodando → Acesse http://localhost:8000 → deve mostrar mensagem
2. Frontend rodando → Acesse http://localhost:3000 → página deve carregar
3. Faça login → deve redirecionar sem erro 422
4. Veja o terminal do backend → deve mostrar log: `🔍 Recebendo login: admin / admin`