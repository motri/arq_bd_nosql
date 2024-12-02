from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['MONGO_URI'] = "mongodb://host.docker.internal:27017/"
    client = MongoClient(app.config['MONGO_URI'])
    app.config['MONGO_DB'] = client['football_awards']
    return app
