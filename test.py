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
    return render_template('index.html')

@app.route('/VerDatos')
def ver_datos():
    # Obtener el número de página actual de los parámetros de consulta
    page = int(request.args.get('page', 1))
    per_page = 10  # Número de elementos por página

    # Calcular el índice de inicio y fin para la consulta en la base de datos
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Obtener el nombre para buscar documentos por el campo 'Name'
    search_name = request.args.get('search_name', '')

    # Realizar la consulta a la base de datos para obtener los datos de la página actual
    if search_name:
        # Si se proporciona un nombre de búsqueda, filtrar los documentos por el campo 'Name'
        query = {'name': {'$regex': search_name, '$options': 'i'}}  # Búsqueda insensible a mayúsculas y minúsculas
        data_from_db = collection.find(query).skip(start_index).limit(per_page)
    else:
        # Si no se proporciona un nombre de búsqueda, obtener todos los documentos
        data_from_db = collection.find().skip(start_index).limit(per_page)

    # Calcular el número total de documentos en la colección
    total_documents = collection.count_documents({})

    # Calcular el número total de páginas
    total_pages = (total_documents + per_page - 1) // per_page

    return render_template('VerDatos.html', data=data_from_db, current_page=page, total_pages=total_pages, search_name=search_name)

@app.route('/delete_document/<string:document_id>', methods=['POST'])
def delete_document(document_id):
    if request.method == 'POST':
        # Eliminar el documento de la base de datos usando document_id
        print(document_id)
        collection.delete_one({"_id": document_id})
        return redirect('/VerDatos')  # Redirigir a la página de ver datos

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

@app.route('/editar_dato/<string:document_id>')
def editar_dato(document_id):
    # Aquí obtienes el documento específico de la base de datos usando document_id
    # Supongamos que lo guardas en una variable llamada document
    document = collection.find_one({"_id": document_id})

    # Verificar si se encontró el documento
    if document:
        # Renderizar la plantilla con el documento como parte de los datos
        return render_template('EditarDato.html', document=document)
    else:
        # Si no se encontró el documento, puedes manejarlo según tu lógica
        return "Documento no encontrado", 404
@app.route('/update_document/<string:document_id>', methods=['POST'])
def update_document(document_id):
    # Obtener los datos actualizados del formulario
    name = request.form['name']
    summary = request.form['summary']
    property_type = request.form['property_type']

    # Actualizar el documento en la base de datos
    collection.update_one(
        {"_id": document_id},
        {"$set": {"name": name, "description": summary, "property_type": property_type}}
    )

    return redirect('/VerDatos')  # Redirigir a la página de ver datos después de la actualización

if __name__ == '__main__':
    app.run(debug=True)
