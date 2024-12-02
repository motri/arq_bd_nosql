import pandas as pd
from pymongo import MongoClient

all_players = pd.read_csv("./data/csv_data/all_players.csv")
gk_players = pd.read_csv("./data/csv_data/gk_players.csv")
all_teams = pd.read_csv("./data/csv_data/all_teams.csv")


client = MongoClient("mongodb://localhost:27017/")
db = client['football_awards']

def load_data():
    players_data = all_players.to_dict('records')
    db['players'].insert_many(players_data)
    
    gk_data = gk_players.to_dict('records')
    db['goalkeepers'].insert_many(gk_data)
    
    teams_data = all_teams.to_dict('records')
    db['teams'].insert_many(teams_data)

load_data()
