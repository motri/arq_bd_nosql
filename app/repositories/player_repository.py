import time

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
            {"$limit": limit}
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
                        {"$multiply": ["$statistics.general.goals", 2.5]},
                        {"$multiply": ["$statistics.general.assists", 2.0]},
                        {"$multiply": ["$statistics.general.minutes_played", 0.5]},
                        {"$multiply": ["$statistics.general.key_passes", 1.5]},
                        {"$multiply": ["$statistics.general.xG", 1.0]},
                        {"$multiply": ["$statistics.general.xA", 1.0]}
                    ]
                }
            }},
            {"$sort": {"ranking_score": -1}},
            {"$limit": limit}
        ]
        result = list(db['players'].aggregate(pipeline))
        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}
