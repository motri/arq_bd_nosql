from flask import Blueprint, request, jsonify
from app.services.players_service import PlayersService

players_blueprint = Blueprint('players_controller', __name__)

@players_blueprint.route('/players/young', methods=['GET'])
def get_young_players():
    age = int(request.args.get('age', 21))
    limit = int(request.args.get('limit', 10))
    db = request.app.config['MONGO_DB']
    result = PlayersService.get_young_players(db, age, limit)
    return jsonify(result), 200

@players_blueprint.route('/players/golden_ball', methods=['GET'])
def get_golden_ball_candidates():
    limit = int(request.args.get('limit', 10))
    db = request.app.config['MONGO_DB']
    result = PlayersService.get_golden_ball_candidates(db, limit)
    return jsonify(result), 200
