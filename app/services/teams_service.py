from repositories import TeamsRepository

class TeamsService:
    @staticmethod
    def get_best_club(db, limit):
        return TeamsRepository.query_best_club(db, limit)
