import json
from pymongo import MongoClient
import pandas as pd

def transform_data_to_json(df):
    transformed_data = []
    for _, row in df.iterrows():
            victory_margin = row.get("Gls", 0) - row.get("G_by_Sh", 0)
            
            # Structure the data
            team_data = {
                "team_name": row.get("Squad", ""),
                "statistics": {
                    "general": {
                        "goals": row.get("Gls", 0),
                        "assists": row.get("Ast", 0),
                        "victory_margin": victory_margin
                    }
                }
            }
            transformed_data.append(team_data)
    return transformed_data

# Transform the data
all_teams = pd.read_csv("./data/csv_data/all_teams.csv")
transformed_teams = transform_data_to_json(all_teams)

def insert_into_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["football_awards"]
    collection = db["teams"]
    result = collection.insert_many(data)
    print(f"Inserted IDs: {result.inserted_ids}")

    print(f"Inserted {len(data)} documents into MongoDB.")

insert_into_mongodb(transformed_teams)

