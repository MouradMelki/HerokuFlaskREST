from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured inserting the store"}, 500 # Internal server error
        return store.json(), 201
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'store deleted'}

    def put(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            store = StoreModel(name)
        else:
            store.price = data['price']
        store.save_to_db()

        return store.json()


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
