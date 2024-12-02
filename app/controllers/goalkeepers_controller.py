from flask import Blueprint, request, jsonify
from app.services.goalkeepers_service import GoalkeepersService

goalkeepers_blueprint = Blueprint('goalkeepers_controller', __name__)

@goalkeepers_blueprint.route('/goalkeepers/golden_glove', methods=['GET'])
def get_golden_glove_candidates():
    limit = int(request.args.get('limit', 10))
    db = request.app.config['MONGO_DB']
    result = GoalkeepersService.get_golden_glove_candidates(db, limit)
    return jsonify(result), 200
