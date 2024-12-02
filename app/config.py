from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    client = MongoClient("mongodb://localhost:27017/")
    app.config['MONGO_CLIENT'] = client
    app.config['MONGO_DB'] = client['football_awards']
    return app
