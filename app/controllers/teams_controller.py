from flask import Blueprint, request, jsonify
from app.services.teams_service import TeamsService

teams_blueprint = Blueprint('teams_controller', __name__)

@teams_blueprint.route('/teams/best', methods=['GET'])
def get_best_club():
    limit = int(request.args.get('limit', 10))
    db = request.app.config['MONGO_DB']
    result = TeamsService.get_best_club(db, limit)
    return jsonify(result), 200
