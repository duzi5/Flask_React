from flask_pymongo import ObjectId
from flask import jsonify, request



class Produto:
    
    def getId(self):
        return ObjectId(self.produto['_id'])

    def deletar(self, collection):
        collection.delete_one(ObjectId(self.produto.getId()))

    def atualizar(self, collection):
        collection.update_one({'_id': ObjectId(self.produto.getId())},{
            '$set': request.json
        })

    def json(self) -> str:
        return jsonify(str(self.produto))
