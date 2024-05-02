# Flask App with MongoDB

This is a Flask app that uses MongoDB as the database. The app allows users to add, view, update, and delete items in the database.

## Installation

To install the app, run the following command:

pip install -r requirements.txt

## Running the App

To run the app, execute the following command:
python app.py

## Configuration

The app uses the following environment variables:

* `MONGODB_URI`: the URI of the MongoDB instance
* `SECRET_KEY`: the secret key for the Flask app

You can set these variables in a `.env` file or as system environment variables.

## Routes

The app has the following routes:

* `/`: the index route that renders the index.html template
* `/VerDatos`: the VerDatos route that displays the data from the database
* `/delete_document/<string:document_id>`: the delete_document route that deletes a document from the database
* `/add_listing`: the add_listing route that adds a new listing to the database

## Templates

The app uses the following templates:

* `index.html`: the index template that displays a form to add a new listing
* `VerDatos.html`: the VerDatos template that displays the data from the database

## Database

The app uses MongoDB as the database. The database is configured using the `MONGODB_URI` environment variable.

## Testing

To run the tests, execute the following command:
python -m unittest discover

## License

This app is licensed under the MIT License.

## Author

[Sergio Ospina - Iker Ballesteros - Mateo Correa - Esteban Escalante]