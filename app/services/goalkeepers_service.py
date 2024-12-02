from repositories import GoalkeepersRepository

class GoalkeepersService:
    @staticmethod
    def get_golden_glove_candidates(db, limit):
        return GoalkeepersRepository.query_golden_glove(db, limit)
