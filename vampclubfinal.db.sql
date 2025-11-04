BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "usuario" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "atleta" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario_id INTEGER,
    FOREIGN KEY(usuario_id) REFERENCES usuario(id)
);
CREATE TABLE IF NOT EXISTS "recomendacao" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    link TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "dias_checkin" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dia INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    local TEXT NOT NULL,
    horario TEXT NOT NULL,
    modalidade TEXT NOT NULL
);

INSERT INTO "atleta" VALUES (1,'mariana oliveira',37,1,'pivo',1);
INSERT INTO "atleta" VALUES (2,'dayane cristina',37,1,'goleira',NULL);
INSERT INTO "atleta" VALUES (3,'fernanda ramos',30,2,'levantadora',NULL);
INSERT INTO "atleta" VALUES (4,'alan ribeiro',31,3,'armador',NULL);
INSERT INTO "atleta" VALUES (5,'Giovana Borghesi',25,2,'Perfil atleta',NULL);
INSERT INTO "evento" VALUES (1,'camiseta',90.0,'ativo',NULL);
INSERT INTO "evento" VALUES (2,'shorts',45.0,'encerrado',NULL);
INSERT INTO "frequencia" VALUES (1,1,1,1);
INSERT INTO "frequencia" VALUES (2,2,3,1);
INSERT INTO "frequencia" VALUES (3,3,2,0);
INSERT INTO "local" VALUES (1,'Sest Senat','Rua Santa Terezinha, R. dos Coqueiros, 1377 - Interlagos, Londrina - PR, 86027-620');
INSERT INTO "local" VALUES (2,'AABB','Av. Cmte. João Ribeiro de Barros, 461 - Bairro Aeroporto, Londrina - PR, 86039-640');
INSERT INTO "modalidade" VALUES (1,'futsal');
INSERT INTO "modalidade" VALUES (2,'volei');
INSERT INTO "modalidade" VALUES (3,'basquete');
INSERT INTO "modalidade" VALUES (4,'futvolei');
INSERT INTO "perfil_usuario" VALUES (1,'admin');
INSERT INTO "perfil_usuario" VALUES (2,'atleta');
INSERT INTO "perfil_usuario" VALUES (3,'treinador');
INSERT INTO "plano" VALUES (1,'bronze',1,0);
INSERT INTO "plano" VALUES (2,'prata',1,1);
INSERT INTO "plano" VALUES (3,'ouro',1,2);
INSERT INTO "plano" VALUES (4,'diamante',1,99);
INSERT INTO "treinador" VALUES (1,'Simões',NULL,NULL);
INSERT INTO "treino" VALUES (1,'09/04/2025','19:00',1,1,NULL);
INSERT INTO "treino" VALUES (2,'16/05/2025','10:30',1,2,NULL);
INSERT INTO "treino" VALUES (3,'24/05/2025','09:00',2,3,NULL);
INSERT INTO "usuario" VALUES (1,'mare.oliveira@icloud.com','1234',2);
INSERT INTO "usuario" VALUES (2,'dayane@gmail.com','abcd',2);
INSERT INTO "usuario" VALUES (3,'fernanda@gmail.com','5678',2);
INSERT INTO "usuario" VALUES (4,'alan@gmail.com','efgh',2);
INSERT INTO "usuario" VALUES (5,'admin','admin',1);
INSERT INTO "usuario" VALUES (6,'simoes@vamp.com','0000',3);
COMMIT;
