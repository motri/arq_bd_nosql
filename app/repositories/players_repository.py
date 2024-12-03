import time
from bson.regex import Regex

class PlayersRepository:
    @staticmethod
    def query_young_players(db, age_threshold=21, limit=10):
        start_time = time.time()
        pipeline = [
            {"$match": {"age": {"$lt": age_threshold}}},
            {"$addFields": {
                "ranking_score": {
                    "$add": [
                        {"$multiply": ["$statistics.general.goals", 2.0]},
                        {"$multiply": ["$statistics.general.assists", 1.0]},
                        {"$multiply": ["$statistics.general.minutes_played", 0.5]}
                    ]
                }
            }},
            {"$sort": {"ranking_score": -1}},
            {"$limit": limit},
            {"$project": {
                "_id": 0,  # Exclude `_id`
                "age": 1,
                "statistics": 1,
                "ranking_score": 1,
                "name": 1
            }}
        ]
        result = list(db['players'].aggregate(pipeline))
        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}

    @staticmethod
    def query_golden_ball(db, limit=10):
        start_time = time.time()
        pipeline = [
            {"$addFields": {
                "ranking_score": {
                    "$add": [
                        {"$multiply": [{"$ifNull": ["$statistics.general.goals", 0]}, 2.5]},
                        {"$multiply": [{"$ifNull": ["$statistics.general.assists", 0]}, 2.0]},
                        {"$multiply": [{"$ifNull": ["$statistics.general.minutes_played", 0]}, 0.5]},
                        {"$multiply": [{"$ifNull": ["$statistics.general.key_passes", 0]}, 1.5]},
                        {"$multiply": [{"$ifNull": ["$statistics.general.xG", 0]}, 1.0]},
                        {"$multiply": [{"$ifNull": ["$statistics.general.xA", 0]}, 1.0]}
                    ]
                }
            }},
            {"$sort": {"ranking_score": -1}},
            {"$limit": limit},
            {"$project": {
                "_id": 0,  
                "name": 1,  
                "statistics": 1,
                "ranking_score": 1
            }}
        ]
        result = list(db['players'].aggregate(pipeline))
        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}


    @staticmethod
    def query_dynamic_players(db, filters, limit):
        start_time = time.time()
        query = {}
        for filter_ in filters:
            field = filter_['field']
            condition = filter_['condition']
            value = filter_['value']

            if condition == "equal":
                query[field] = value
            elif condition == "bigger":
                query[field] = {"$gt": value}
            elif condition == "smaller":
                query[field] = {"$lt": value}
            elif condition == "contains":
                query[field] = {"$regex": "Manchester", "$options": "i"} 

        # Execute the query
        result = list(db['players'].find(query).limit(limit))
        for doc in result:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}