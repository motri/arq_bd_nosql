import pandas as pd
from pymongo import MongoClient
import json


gk_data = pd.read_csv("./data/csv_data/all_players.csv")

def transform_gk_data_to_json(df):
    documents = []
    for _, row in df.iterrows():
        document = {
            "name": row.get("Player", ""),
            "position": "GK",  # As per the query, we're dealing with goalkeepers only
            "statistics": {
                "goalkeeper": {
                    "saves": row.get("Saves", 0) if pd.notnull(row.get("Saves")) else 0,
                    "penalty_saves": row.get("PenaltySaves", 0) if pd.notnull(row.get("PenaltySaves")) else 0
                },
                "general": {
                    "minutes_played": row.get("MinutesPlayed", 0) if pd.notnull(row.get("MinutesPlayed")) else 0
                }
            }
        }
        documents.append(document)
    return documents

# Transform the data
goalkeeper_documents = transform_gk_data_to_json(gk_data)


def insert_into_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["football_awards"]
    collection = db["goalkeepers"]
    result = collection.insert_many(data)
    print(f"Inserted IDs: {result.inserted_ids}")

    print(f"Inserted {len(data)} documents into MongoDB.")

insert_into_mongodb(goalkeeper_documents)
