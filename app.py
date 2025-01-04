from flask import Flask, request, jsonify, render_template, session
import numpy as np
import pandas as pd
import random
from Jogadores import Jogadores
from Partidas import Partidas

j = Jogadores()
p = Partidas()
app = Flask(__name__)

app.secret_key = 'dasdasdasdasdsadsd78as7d9as7d9as7d987as9d8'


# Variáveis globais para gerenciar o jogo
jogo = None
jogador_atual = "X"
trava = False

@app.route('/')
def index():
    global jogo
    jogo = None
    return render_template("jogadores.html")

@app.route('/telajogo/<int:id>')
def telajogo(id):
   global trava
   trava = False
   session['idjogador'] = id
   nome = j.getnome(id)[0]['nome']
   return render_template("tela.html", nome = nome)


@app.route('/cadastrarjogador', methods=['POST'])
def cadastrarjogador():
    dados = request.get_json()
    return j.cadastrar(nome=dados.get('nome'))

@app.route('/deletarjogador/<int:id>', methods=['DELETE'])
def deletarjogador(id):
    return jsonify(j.deletar(id))


@app.route('/listarjogadores', methods=['GET'])
def listarjogadores():
    return jsonify(j.listartodos())


@app.route('/tabuleiro', methods=['GET'])
def tabuleiro():
    global jogo
    if jogo is None:
        jogo = np.array([[None, None, None],
                         [None, None, None],
                         [None, None, None]])
    return pd.DataFrame(jogo).to_json()


@app.route('/jogar', methods=['POST'])
def jogar():
    global jogo, jogador_atual, trava

    if trava == True:
        return {"erro": "Jogo finalizado, inicie um novo jogo."}, 400

    if jogo is None:
        return jsonify(
            {"erro": "O tabuleiro não foi inicializado."}), 400

    dados = request.get_json()
    x, y = dados.get("x"), dados.get("y")

    if x is None or y is None:
        return jsonify({"erro": "Coordenadas inválidas. Forneça valores para 'x' e 'y'."}), 400

    if not (0 <= x < 3 and 0 <= y < 3):
        return jsonify({"erro": "As coordenadas devem estar entre 0 e 2."}), 400

    if jogo[x, y] is not None:
        return jsonify({"erro": "Essa posição já está ocupada."}), 400

    jogo[x, y] = jogador_atual


    if(np.sum(jogo == None) > 1):
        while True:
            xo = random.randint(0, 2)
            yo = random.randint(0, 2)
            if(jogo[xo, yo] is not None):
                continue
            jogo[xo, yo] = "O"
            break

    if verificar_vencedor("X"):
        trava = True
        p.cadastrar(pd.DataFrame(jogo).to_json(), 'V', session['idjogador'])
        return jsonify({"mensagem": f"venceu"}), 200
    
    if verificar_vencedor("O"):
        trava = True
        p.cadastrar(pd.DataFrame(jogo).to_json(), 'P', session['idjogador'])
        return jsonify({"mensagem": f"perdeu"}), 200

    return pd.DataFrame(jogo).to_json()

@app.route('/novojogo', methods=['GET'])
def novojogo():
    global jogo, trava
    jogo = None
    trava = False
    return jsonify({"mensagem": f"Novo jogo iniciado!"}), 200


def verificar_vencedor(jogador):
    for i in range(3):
        if all(jogo[i, :] == jogador) or all(jogo[:, i] == jogador):
            return True
    if all(jogo.diagonal() == jogador) or all(np.fliplr(jogo).diagonal() == jogador):
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)