from flask import Blueprint, request, jsonify, current_app
from services import TeamsService

teams_blueprint = Blueprint('teams_controller', __name__)

@teams_blueprint.route('/teams/best', methods=['GET'])
def get_best_club():
    limit = int(request.args.get('limit', 10))
    db = current_app.config['MONGO_DB'] 
    result = TeamsService.get_best_club(db, limit)
    return jsonify(result), 200
