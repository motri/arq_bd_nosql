from pymongo import MongoClient

class MongoRepository:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client["players"]
        self.collection = self.db["all_stats"]