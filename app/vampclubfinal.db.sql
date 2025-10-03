BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "atleta" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	"idade"	INTEGER,
	"modalidade_id"	INTEGER,
	"dados_tecnicos"	TEXT,
	"usuario_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("usuario_id") REFERENCES "usuario"("id")
);
CREATE TABLE IF NOT EXISTS "atleta_modalidade" (
	"atleta_id"	INTEGER,
	"modalidade_id"	INTEGER,
	PRIMARY KEY("atleta_id","modalidade_id"),
	FOREIGN KEY("atleta_id") REFERENCES "atleta"("id"),
	FOREIGN KEY("modalidade_id") REFERENCES "modalidade"("id")
);
CREATE TABLE IF NOT EXISTS "evento" (
	"id"	INTEGER,
	"tipo"	TEXT NOT NULL,
	"valor"	REAL,
	"status"	TEXT,
	"data"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "frequencia" (
	"id"	INTEGER,
	"atleta_id"	INTEGER,
	"treino_id"	INTEGER,
	"presente"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("atleta_id") REFERENCES "atleta"("id"),
	FOREIGN KEY("treino_id") REFERENCES "treino"("id")
);
CREATE TABLE IF NOT EXISTS "local" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	"endereco"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "modalidade" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "padrao_treino" (
	"id"	INTEGER,
	"nivel"	TEXT,
	"modalidade_id"	INTEGER,
	"dia_semana"	TEXT,
	"horario"	NUMERIC,
	PRIMARY KEY("id"),
	CONSTRAINT "modalidade" FOREIGN KEY("modalidade_id") REFERENCES ""
);
CREATE TABLE IF NOT EXISTS "perfil_usuario" (
	"id"	INTEGER,
	"nome"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "plano" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	"acesso_aulas"	INTEGER NOT NULL,
	"acesso_modalidades"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "treinador" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	"usuario_id"	INTEGER,
	"especialidade"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("usuario_id") REFERENCES "usuario"("id")
);
CREATE TABLE IF NOT EXISTS "treinador_modalidade" (
	"treinador_id"	INTEGER,
	"modalidade_id"	INTEGER,
	PRIMARY KEY("treinador_id","modalidade_id"),
	FOREIGN KEY("modalidade_id") REFERENCES "modalidade"("id"),
	FOREIGN KEY("treinador_id") REFERENCES "treinador"("id")
);
CREATE TABLE IF NOT EXISTS "treino" (
	"id"	INTEGER,
	"data"	TEXT NOT NULL,
	"horario"	TEXT NOT NULL,
	"local_id"	INTEGER NOT NULL,
	"modalidade_id"	INTEGER,
	"status"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("local_id") REFERENCES "local"("id"),
	FOREIGN KEY("modalidade_id") REFERENCES "modalidade"("id")
);
CREATE TABLE IF NOT EXISTS "usuario" (
	"id"	INTEGER,
	"email"	TEXT NOT NULL,
	"senha"	TEXT NOT NULL,
	"perfil_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("perfil_id") REFERENCES "perfil_usuario"("id")
);
INSERT INTO "atleta" VALUES (1,'mariana oliveira',37,1,'pivo',1);
INSERT INTO "atleta" VALUES (2,'dayane cristina',37,1,'goleira',NULL);
INSERT INTO "atleta" VALUES (3,'fernanda ramos',30,2,'levantadora',NULL);
INSERT INTO "atleta" VALUES (4,'alan ribeiro',31,3,'armador',NULL);
INSERT INTO "atleta" VALUES (5,'Giovana Borghesi',25,2,'Perfil atleta',NULL);
INSERT INTO "atleta_modalidade" VALUES (5,2);
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
