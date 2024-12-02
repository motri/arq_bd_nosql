import time

class GoalkeepersRepository:
    @staticmethod
    def query_golden_glove(db, limit=10):
        start_time = time.time()
        pipeline = [
            {"$match": {"position": "GK"}},
            {"$addFields": {
                "ranking_score": {
                    "$add": [
                        {"$multiply": ["$statistics.goalkeeper.saves", 2.0]},
                        {"$multiply": ["$statistics.goalkeeper.penalty_saves", 1.5]},
                        {"$multiply": ["$statistics.general.minutes_played", 0.5]}
                    ]
                }
            }},
            {"$sort": {"ranking_score": -1}},
            {"$limit": limit}
        ]
        result = list(db['goalkeepers'].aggregate(pipeline))
        elapsed_time = time.time() - start_time
        return {"data": result, "execution_time": elapsed_time}
