import time

class TeamsRepository:
    @staticmethod
    def query_best_club(db, limit=10):
        start_time = time.time()
        pipeline = [
            {"$addFields": {
                "ranking_score": {
                    "$add": [
                        {"$multiply": ["$statistics.general.goals", 3.0]},
                        {"$multiply": ["$statistics.general.assists", 2.0]},
                        {"$multiply": ["$statistics.team.victory_margin", 1.0]}
                    ]
                }
            }},
            {"$sort": {"ranking_score": -1}},
            {"$limit": limit}
        ]
        result = list(db['teams'].aggregate(pipeline))
        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}
