import json
from pymongo import MongoClient
import pandas as pd
import random

def transform_data_to_json(df):
    players_json = []
    for _, row in df.iterrows():
        age_raw = str(row.get("Age", ""))
        age = int(age_raw.split('-')[0]) if '-' in age_raw else None
        player_data = {
            "name": row.get("Player"),
            "nation": row.get("Nation"),
            "position": row.get("Pos"),
            "squad": row.get("Squad"),
            "age": age,
            "debut": row.get("Born", 0)+ 18 + random.randint(0, 3),
            "statistics": {
                "general": {
                    "matches_played": row.get("MP"),
                    "starts": row.get("Starts"),
                    "minutes_played": row.get("Min"),
                    "goals": row.get("Gls"),
                    "assists": row.get("Ast"),
                },
                "advanced": {
                    "offsides": row.get("Off"),
                    "crosses": row.get("Crs"),
                    "tackles_won": row.get("TklW"),
                    "penalties_won": row.get("PKwon"),
                    "penalties_conceded": row.get("PKcon"),
                    "own_goals": row.get("OG"),
                    "recoveries": row.get("Recov"),
                    "aerial_duels": {
                        "won": row.get("AerialDuels_Won"),
                        "lost": row.get("AerialDuels_Lost"),
                    },
                    "completed_passes": row.get("Cmp"),
                },
            },
        }
        players_json.append(player_data)
    return players_json

# Transform the data
all_players = pd.read_csv("../data/csv_data/all_players.csv")
transformed_data = transform_data_to_json(all_players)

def insert_into_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["football_awards"]
    collection = db["players"]
    result = collection.insert_many(data)
    print(f"Inserted IDs: {result.inserted_ids}")

    print(f"Inserted {len(data)} documents into MongoDB.")

insert_into_mongodb(transformed_data)

