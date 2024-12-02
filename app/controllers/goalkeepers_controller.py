from flask import Blueprint, request, jsonify, current_app
from services import GoalkeepersService

goalkeepers_blueprint = Blueprint('goalkeepers_controller', __name__)

@goalkeepers_blueprint.route('/golden_glove', methods=['GET'])
def get_golden_glove_candidates():
    limit = int(request.args.get('limit', 10))
    db = current_app.config['MONGO_DB']
    result = GoalkeepersService.get_golden_glove_candidates(db, limit)
    return jsonify(result), 200
