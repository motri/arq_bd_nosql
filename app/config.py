from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# Flask App and MongoDB configuration
def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # MongoDB configuration
    client = MongoClient("mongodb://localhost:27017/")
    app.config['MONGO_CLIENT'] = client
    app.config['MONGO_DB'] = client['football_awards']
    
    return app
