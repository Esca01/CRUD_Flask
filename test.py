from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB setup
uri = "mongodb+srv://crudistribuidos:eSbSo25tgf15pT49@clusterd.fb0ybuu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterD"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sample_airbnb']
collection = db['listingsAndReviews']

@app.route('/')
def index():
    # Obtener los primeros diez documentos de la colección
    data_from_db = collection.find().limit(10)

    # Filtrar los campos que se mostrarán en la página web
    filtered_data = []
    for document in data_from_db:
        filtered_document = {
            "_id": document["_id"],
            "listing_url": document.get("listing_url", ""),
            "name": document.get("name", ""),
            "summary": document.get("summary", ""),
            "property_type": document.get("property_type", "")
        }
        filtered_data.append(filtered_document)
    
    # Renderizar la plantilla HTML con los datos filtrados obtenidos de la base de datos
    return render_template('index.html', data=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
