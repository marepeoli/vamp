BEGIN TRANSACTION;

-- VampClub Database Schema
-- Sistema de gerenciamento de treinos e eventos esportivos

-- Tabela de usuários para login
CREATE TABLE IF NOT EXISTS login_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela principal de usuários
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de usuários (sistema secundário)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de eventos
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de treinos
CREATE TABLE IF NOT EXISTS treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,               -- ISO date YYYY-MM-DD
    hora TEXT NOT NULL,
    modalidade TEXT NOT NULL,
    local TEXT NOT NULL,
    vagas_total INTEGER NOT NULL,
    vagas_disponiveis INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de check-ins
CREATE TABLE IF NOT EXISTS checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    treino_id INTEGER NOT NULL,
    usuario_email TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY(treino_id) REFERENCES treinos(id)
);

-- Dados iniciais de usuários de teste
INSERT OR IGNORE INTO usuario (nome, email, senha) VALUES 
    ('Mariana Oliveira', 'mare.oliveira@icloud.com', '123456'),
    ('Dayane Silva', 'dayane@gmail.com', '123456'),
    ('João Santos', 'joao@gmail.com', '123456');

-- Usuário admin padrão
INSERT OR IGNORE INTO login_users (username, password) VALUES 
    ('admin', 'admin');

-- Eventos de exemplo
INSERT OR IGNORE INTO events (title, description, date, location) VALUES 
    ('Campeonato InterVamp 2025', 'Campeonato interno de todas as modalidades', '2025-02-15', 'Quadras A e B'),
    ('Treino Especial de Verão', 'Treino intensivo preparatório para o verão', '2025-01-20', 'Quadra A'),
    ('Torneio de Futsal', 'Torneio eliminatório de futsal', '2025-03-10', 'Quadra B');

COMMIT;
