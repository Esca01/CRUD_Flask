from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB setup
uri = "mongodb+srv://crudistribuidos:eSbSo25tgf15pT49@clusterd.fb0ybuu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterD"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sample_airbnb']
collection = db['listingsAndReviews']


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
@app.route('/')
def index():
    # Renderizar la plantilla HTML con los datos filtrados obtenidos de la base de datos
    return render_template('index.html', data=filtered_data)

@app.route('/add_listing', methods=['POST'])
def add_listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        property_type = request.form['property_type']
        
        # Guardar los datos en la base de datos
        new_listing = {
            "name": name,
            "description": description,
            "property_type": property_type
        }
        collection.insert_one(new_listing)
        
        return redirect('/')  # Redirigir a la página principal después de agregar el listado

@app.route('/AñadirDato')
def add_data_page():
    return render_template('AñadirDato.html')

if __name__ == '__main__':
    app.run(debug=True)
