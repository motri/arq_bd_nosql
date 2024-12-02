from pymongo import MongoClient

def create_db_and_collections():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    
    # Create database
    db = client['football_awards']
    
    # Explicitly create collections
    db.create_collection("players")
    db.create_collection("goalkeepers")
    db.create_collection("teams")
    
    print("Database and collections created successfully!")
    
if __name__ == "__main__":
    create_db_and_collections()
