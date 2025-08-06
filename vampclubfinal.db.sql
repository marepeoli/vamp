BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "atleta" (
	"id"	INTEGER,
	"nome"	TEXT NOT NULL,
	"idade"	INTEGER,
	"modalidade_id"	INTEGER,
	"dados_tecnicos"	TEXT,
	"usuario_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("modalidade_id") REFERENCES "modalidade"("id"),
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
	"modalidade_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("modalidade_id") REFERENCES "modalidade"("id")
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("local_id") REFERENCES "local"("id"),
	FOREIGN KEY("modalidade_id") REFERENCES "modalidade"("id")
);
CREATE TABLE IF NOT EXISTS "usuario" (
	"id"	INTEGER,
	"cpf"	INTEGER UNIQUE,
	"email"	TEXT UNIQUE,
	"plano_id"	INTEGER,
	"senha"	TEXT,
	"perfil"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("plano_id") REFERENCES "plano"("id")
);
INSERT INTO "atleta" VALUES (1,'mariana oliveira',37,1,'pivo',1);
INSERT INTO "atleta" VALUES (2,'dayane cristina',37,1,'goleira',NULL);
INSERT INTO "atleta" VALUES (3,'fernanda ramos',30,2,'levantadora',NULL);
INSERT INTO "atleta" VALUES (4,'alan ribeiro',31,3,'armador',NULL);
INSERT INTO "evento" VALUES (1,'camiseta',90.0,'ativo');
INSERT INTO "evento" VALUES (2,'shorts',45.0,'encerrado');
INSERT INTO "frequencia" VALUES (1,1,1,1);
INSERT INTO "frequencia" VALUES (2,2,3,1);
INSERT INTO "frequencia" VALUES (3,3,2,0);
INSERT INTO "modalidade" VALUES (1,'futsal');
INSERT INTO "modalidade" VALUES (2,'volei');
INSERT INTO "modalidade" VALUES (3,'basquete');
INSERT INTO "modalidade" VALUES (4,'futvolei');
INSERT INTO "plano" VALUES (1,'bronze',1,0);
INSERT INTO "plano" VALUES (2,'prata',1,1);
INSERT INTO "plano" VALUES (3,'ouro',1,2);
INSERT INTO "plano" VALUES (4,'diamante',1,99);
INSERT INTO "treinador" VALUES (1,'Simões',1);
INSERT INTO "treino" VALUES (1,'09/04/2025','19:00','Sest Senat',1);
INSERT INTO "treino" VALUES (2,'16/05/2025','10:30','Sest Senat',2);
INSERT INTO "treino" VALUES (3,'24/05/2025','09:00','AABB',3);
INSERT INTO "usuario" VALUES (1,7077665917,'mare.oliveira@icloud.com',4,'1234',NULL);
INSERT INTO "usuario" VALUES (2,123456789,'dayane@gmail.com',2,'abcd',NULL);
INSERT INTO "usuario" VALUES (3,321654987,'fernanda@gmail.com',1,'5678',NULL);
INSERT INTO "usuario" VALUES (4,987654321,'alan@gmail.com',3,'efgh',NULL);
COMMIT;
