import sqlite3

class DBManager:
    def __init__(self, db_name="vampclubfinal.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_atletas(self):
        self.cursor.execute("SELECT * FROM atleta")
        return self.cursor.fetchall()

    def add_treinador(self, nome, modalidade_id):
        self.cursor.execute("INSERT INTO treinador (nome, modalidade_id) VALUES (?, ?)", (nome, modalidade_id))
        self.conn.commit()

    def get_modalidades(self):
        self.cursor.execute("SELECT * FROM modalidade")
        return self.cursor.fetchall()
        
    def validate_login(self, email, senha):
        self.cursor.execute("SELECT * FROM usuario WHERE email = ? AND senha = ?", (email, senha))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

    def add_atleta(self, nome, idade, modalidade_id, dados_tecnicos, usuario_id=None):
        self.cursor.execute(
            "INSERT INTO atleta (nome, idade, modalidade_id, dados_tecnicos, usuario_id) VALUES (?, ?, ?, ?, ?)",
            (nome, idade, modalidade_id, dados_tecnicos, usuario_id)
        )
        self.conn.commit()
