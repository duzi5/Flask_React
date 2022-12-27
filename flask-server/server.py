from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_pymongo import ObjectId
from flask_cors import CORS
from produtos import *
import json 
from bson.json_util import dumps

app = Flask(__name__)
URI = "mongodb+srv://duzis:duzis@cluster0.fwzx7jb.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(URI)
collectionProdutos = mongo.testando.produtos
collectionUsers = mongo.testando.users

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

@app.route("/produto/<id>", methods=["GET"] )
def produto(id):
    return dumps(collectionProdutos.find_one({"_id" : ObjectId(id)}))
     
# USUÁRIOS #######################

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    return dumps(user = collectionUsers.find_one({
        '_id': ObjectId(id)
    }))
    
@app.route('/user/<id>', methods=['PUT'])
def putUser(id):
    user = collectionUsers.update_one({'_id': ObjectId(id)},{
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