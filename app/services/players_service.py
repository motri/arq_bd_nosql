from repositories import PlayersRepository

class PlayersService:
    @staticmethod
    def get_young_players(db, age_threshold, limit):
        return PlayersRepository.query_young_players(db, age_threshold, limit)

    @staticmethod
    def get_golden_ball_candidates(db, limit):
        return PlayersRepository.query_golden_ball(db, limit)

    @staticmethod
    def query_dynamic(db, filters, limit):
        return PlayersRepository.query_dynamic_players(db, filters, limit)
