from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import os

# Initialize Flask and Flask-RESTful
app = Flask(__name__)
api = Api(app)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI', 'your-default-mongo-uri')
client = MongoClient(mongo_uri)
db = client['']  # Replace with your database name
collection = db['your-collection-name']  # Replace with your collection name

# Define a resource for the Item
class Item(Resource):
    def get(self, item_id):
        # Retrieve an item by ID
        item = collection.find_one({"_id": item_id})
        if item:
            return item, 200
        else:
            return {"message": "Item not found"}, 404

    def post(self):
        # Create a new item
        data = request.get_json()  # Data should be in JSON format
        collection.insert_one(data)
        return data, 201

    def put(self, item_id):
        # Update an existing item
        data = request.get_json()
        result = collection.update_one({"_id": item_id}, {"$set": data})
        if result.modified_count > 0:
            return data, 200
        else:
            return {"message": "No changes made"}, 404

    def delete(self, item_id):
        # Delete an item
        result = collection.delete_one({"_id": item_id})
        if result.deleted_count > 0:
            return {"message": "Item deleted"}, 204
        else:
            return {"message": "Item not found"}, 404

# Add the Item resource to the API and specify the route
api.add_resource(Item, '/item/<string:item_id>')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
