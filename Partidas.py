import sqlite3

class Partidas:
    
    def __init__(self, db_path='db.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários

    def cadastrar(self, partida, status, id_jogador):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO partidas (partida, status, id_jogador) VALUES (?, ?, ?)", (partida, status, id_jogador,))
            self.conn.commit()
            return {"message": "jogador adicionado com sucesso"}
        except Exception as e:
            return {"error": str(e)}