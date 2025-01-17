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
        
    def deletar(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM jogadores WHERE id = ?", (id,))
            cursor.execute("DELETE FROM partidas WHERE id_jogador = ?", (id,))
            self.conn.commit()
            return {"message": "jogador deletado com sucesso"}
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
        
    def getnome(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT nome FROM jogadores where id = ?", (id,))
            nome = cursor.fetchall()
            return [dict(j) for j in nome]
        except Exception as e:
            return {"error": str(e)}
        
    def estatisticas(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            select
            case when status = 'V' then 'venceu'
            when status = 'P' then 'perdeu'
            else 'empatou'
            end as status,
            count(p.id) as quantidade
            from jogadores as j
            inner join partidas as p 
            on j.id = p.id_jogador 
            where j.id = ?
            group by status
            ''', (id,))
            res = cursor.fetchall()
            return [dict(j) for j in res]
        except Exception as e:
            return {"error": str(e)}