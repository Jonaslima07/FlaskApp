from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

propriedadesGlobal = [
    {'id': 1, 'nome': 'Sítio Lajes', 'cidade': 'Solânea'},
    {'id': 2, 'nome': 'Sítio Titara'},
    {'id': 3, 'nome': 'Poço Escuro'}
]


def getConnection():
    # 1 - Conectar.
    return sqlite3.connect('agricolaif.db')


@app.route("/")
def homeResource():
    aplicacao = {'versao': '1.0'}
    return jsonify(aplicacao), 200


def encotrarMaiorId():
    maiorId = 0
    for propriedade in propriedadesGlobal:
        if (propriedade['id'] > maiorId):
            maiorId = propriedade['id']
    return maiorId


def calcularProximoId():
    return encotrarMaiorId() + 1


@app.get("/propriedades")
def propriedades_get():
    try:
        # 1 - Conectar.
        connection = sqlite3.connect('agricolaif.db')
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from tb_propriedades")
        # 4 - retorna resultset
        resultset = cursor.fetchall()
        # Iterar e transformar dados.
        propriedades = []
        for item in resultset:
            propriedade = {'id': item[0], 'nome': item[1], 'cidade': item[2]}
            propriedades.append(propriedade)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 5 - Fechar conexão.
        connection.close()
    return jsonify(propriedades), 200


@app.post("/propriedades")
def propriedades_post():
    # Captar o json da requisição e adicionar na lista.
    propriedadeNova = request.json

    # Manipulação do dados antiga.
    # propriedadeNova['id'] = calcularProximoId()
    # propriedades.append(propriedadeNova)
    # 1 - Conectar.
    connection = sqlite3.connect('agricolaif.db')

    # 2 - Obter cursor.
    cursor = connection.cursor()

    # 3 - Executar.
    cursor.execute(
        "insert into tb_propriedades(nome, cidade) values (?, ?)", (propriedadeNova['nome'], propriedadeNova['cidade']))

    # 3.1 - Confirmar - commit.
    connection.commit()

    id = cursor.lastrowid
    propriedadeNova['id'] = id

    # 4 - Fechar conexão.
    connection.close()

    return jsonify(propriedadeNova), 200


def getPropriedadeById(idPropriedade):
    try:
        # Retornar o resultset.
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # 3 - Executar.
        cursor.execute(
            "select * from tb_propriedades where id = ?", (idPropriedade,))
        # 4 - Retornar resultset
        resultset = cursor.fetchone()  # [] -> ()
    finally:
        # 5 - Fechar conexão.
        connection.close()
    return resultset


@app.get("/propriedades/<int:idPropriedade>")
def propriedade_get(idPropriedade):
    try:
        resultset = getPropriedadeById(idPropriedade)
        # Transformar dados.
        if resultset is not None:
            propriedade = {
                'id': resultset[0], 'nome': resultset[1], 'cidade': resultset[2]}
        else:
            return (jsonify({'mensagem': 'Propriedade não encontrada'}), 404)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(propriedade), 200


@app.put("/propriedades/<int:idPropriedade>")
def propriedades_put(idPropriedade):
    try:
        # Captar o json da requisição e adicionar na lista.
        propriedadeAtualizada = request.json
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Verificar se a pripriedade a ser atualizada existe.
        resultset = getPropriedadeById(idPropriedade)
        if resultset is not None:
            # 3 - Executar.
            cursor.execute("update tb_propriedades set nome = ?, cidade=? where id=?",
                           (propriedadeAtualizada['nome'], propriedadeAtualizada['cidade'], idPropriedade))
            # 3.1 - Confirmar - commit.
            connection.commit()
            # Adicionar id ao json.
            propriedadeAtualizada['id'] = idPropriedade
            return jsonify(propriedadeAtualizada), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 5 - Fechar conexão.
        connection.close()

    return (jsonify({'mensagem': 'Propriedade não encontrada'}), 404)


@app.delete("/propriedades/<int:idPropriedade>")
def propriedades_delete(idPropriedade):
    try:
        # 1 - Conectar.
        connection = getConnection()
        # 2 - Obter cursor.
        cursor = connection.cursor()
        # Verificar se a pripriedade a ser atualizada existe.
        resultset = getPropriedadeById(idPropriedade)
        print(resultset)
        # if resultset is not None:
        if resultset is None:
            return (jsonify({'mensagem': 'Propriedade não encontrada'}), 404)
            # 3 - Executar.
        cursor.execute(
                "delete from tb_propriedades where id = ?", (idPropriedade, ))
            # 3.1 - Confirmar - commit.
        connection.commit()
        return {'mensagem': "Removido com sucesso"}, 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 5 - Fechar conexão.
        connection.close()