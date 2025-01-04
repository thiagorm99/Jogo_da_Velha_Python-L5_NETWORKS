import sqlite3

class Jogadores:
    
    def __init__(self, db_path='db.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários

    def cadastrar(self, nome):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO jogadores (nome) VALUES (?)", (nome,))
            self.conn.commit()
            return {"message": "jogador adicionado com sucesso"}
        except Exception as e:
            return {"error": str(e)}
        
    def listartodos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM jogadores")
            jogadres = cursor.fetchall()
            return [dict(j) for j in jogadres]
        except Exception as e:
            return {"error": str(e)}