BEGIN TRANSACTION;
-- Criar tabela treinos se não existir
CREATE TABLE IF NOT EXISTS treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    modalidade TEXT NOT NULL,
    local TEXT NOT NULL,
    vagas_total INTEGER NOT NULL,
    vagas_disponiveis INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela usuario para o login (caso não exista)
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela checkins se não existir
CREATE TABLE IF NOT EXISTS checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    treino_id INTEGER NOT NULL,
    usuario_email TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY(treino_id) REFERENCES treinos(id)
);

-- Limpar treinos existentes para evitar duplicatas
DELETE FROM treinos;

-- Inserir treinos para os sábados de novembro/dezembro 2024 (próximos sábados)
INSERT INTO treinos (data, hora, modalidade, local, vagas_total, vagas_disponiveis) VALUES
('2024-11-02', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-11-09', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-11-16', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-11-23', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-11-30', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-12-07', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-12-14', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-12-21', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12),
('2024-12-28', '09:00', 'Futsal Avançado', 'Sest Senat', 12, 12);

-- Inserir usuário de teste para login
INSERT OR IGNORE INTO usuario (nome, email, senha) VALUES
('Mariana Oliveira', 'mariana@vamp.com', '123456'),
('Usuario Teste', 'teste@vamp.com', 'senha123'),
('Admin', 'admin@vamp.com', 'admin');

COMMIT;
