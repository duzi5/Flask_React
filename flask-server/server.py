from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from flask_pymongo import ObjectId
from flask_cors import CORS
from produtos import *
import json
import os
from bson.json_util import dumps
from random import random 
from pathlib import Path

app = Flask(__name__)
URI = "mongodb+srv://duzis:duzis@cluster0.fwzx7jb.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(URI)
collectionProdutos = mongo.testando.produtos
collectionUsers = mongo.testando.users

# SLIDES #######################

@app.route('/lista_slides', methods=['GET'])
def lista_slides():
    slides = []
    for nome_do_arquivo in os.listdir('slides'):
        endereco_do_arquivo = os.path.join('./slides/' + nome_do_arquivo)
        if (os.path.isfile(endereco_do_arquivo)):
            slides.append(nome_do_arquivo)
    return jsonify(slides)

@app.route('/manda_slides', methods=['POST'])
def manda_slides():
    print(request.files)
    slide = request.files.get('slide')
    upload_name =  slide.filename
    slide.save(os.path.join('./slides/'+ upload_name))
    return "Imagem de slide enviada com sucesso"


@app.route('/slide/<nome_do_slide>', methods=[ 'GET'])
def pega_slide(nome_do_slide):
    return send_from_directory("./slides/" + nome_do_slide, as_attachment=False)


@app.route('/slide/<nome_do_slide>', methods=['DELETE'])
def deleta_slide(nome_do_slide):    
    slide = os.path.join('./slides/' + nome_do_slide)
    if slide:
        os.remove(slide)
        return "Deletado com sucesso!"
    else: 
        return "Item não encontrado, não existe slide com esse nome.", 404

# ARQUIVOS #######################

@app.route('/arquivo', methods=['POST'])
def mandaArquivo():
    arquivo = request.files.get('imagem')
    nome_do_arquivo = request.files.get('imagem').filename
    print(nome_do_arquivo)

    arquivo.save(os.path.join('./imagens/' + nome_do_arquivo))

    return "cheguei aqui"


@app.route('/arquivos', methods=['GET'])
def lista_arquivos():
    arquivos = []

    for nome_do_arquivo in os.listdir('imagens'):
        endereco_do_arquivo = os.path.join('./imagens/' + nome_do_arquivo)
        if (os.path.isfile(endereco_do_arquivo)):
            arquivos.append(nome_do_arquivo)
    return jsonify(arquivos)


@app.route("/arquivo/<nome_do_arquivo>", methods=["GET"])
def get_arquivo(nome_do_arquivo):
    return send_from_directory('./imagens/', nome_do_arquivo, as_attachment=False)


# PRODUTOS #######################


@app.route('/produtos', methods=['POST'])
def adicionar():
    collectionProdutos.insert_one(request.json)

    return "Adicionado"


@app.route('/produtos/<id>', methods=['PUT'])
def editar(id):
    produto = collectionProdutos.find_one({"_id": ObjectId(id)}, request.json)
    return "Editado"


@app.route('/produtos/<id>', methods=['DELETE'])
def deletar(id):
    collectionProdutos.delete_one({"_id": ObjectId(id)})
    return "Deletado"


@app.route("/produtos", methods=["GET"])
def visualizarTodos():
    return dumps(collectionProdutos.find())


@app.route("/produto/<id>", methods=["GET"])
def produto(id):
    return dumps(collectionProdutos.find_one({"_id": ObjectId(id)}))

# USUÁRIOS #######################


@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    return dumps(user=collectionUsers.find_one({
        '_id': ObjectId(id)
    }))


@app.route('/user/<id>', methods=['PUT'])
def putUser(id):
    user = collectionUsers.update_one({'_id': ObjectId(id)}, {
        '$set': request.json
    })


@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    user = collectionUsers.delete_one({
        '_id': ObjectId(id)
    })
    return "Deletado"


@app.route('/users', methods=['POST'])
def createUser():
    collectionUsers.insert_one(request.json)
    return "received"


@app.route('/users', methods=['GET'])
def lista():
    return dumps(collectionUsers.find())


if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, debug=True)
