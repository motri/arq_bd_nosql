import time

class TeamsRepository:
    @staticmethod
    def query_best_club(db, limit=10):
        start_time = time.time()
        pipeline = [
            {"$addFields": {
                "ranking_score": {
                    "$add": [
                        {"$multiply": ["$statistics.general.goals", 2.5]},
                        {"$multiply": ["$statistics.general.assists", 2.0]},
                        {"$multiply": ["$statistics.general.victory_margin", 1.5]},
                    ]
                }
            }},
            {"$sort": {"ranking_score": -1}},
            {"$limit": limit},
            {"$project": {
                "_id": 0,
                "team_name": 1,
                "ranking_score": 1,
                "statistics": 1
            }}
        ]
        result = list(db['teams'].aggregate(pipeline))
        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}
