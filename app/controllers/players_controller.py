from flask import Blueprint, request, jsonify, current_app
from services import PlayersService

players_blueprint = Blueprint('players_controller', __name__)

@players_blueprint.route('/young', methods=['GET'])
def get_young_players():
    age = int(request.args.get('age', 21))
    limit = int(request.args.get('limit', 10))
    db = current_app.config['MONGO_DB']
    result = PlayersService.get_young_players(db, age, limit)
    return jsonify(result), 200

@players_blueprint.route('/golden_ball', methods=['GET'])
def get_golden_ball_candidates():
    limit = int(request.args.get('limit', 10))
    db = current_app.config['MONGO_DB']
    result = PlayersService.get_golden_ball_candidates(db, limit)
    return jsonify(result), 200

@players_blueprint.route('/query', methods=['GET'])
def query_players():
    try:
        db = current_app.config['MONGO_DB']
        filters = []
        limit = int(request.args.get('limit', 10)) 

        query_params = request.args.to_dict(flat=False)  
        fields = query_params.get('field', [])
        conditions = query_params.get('condition', [])
        values = query_params.get('value', [])

        for field, condition, value in zip(fields, conditions, values):
            filters.append({
                "field": field,
                "condition": condition,
                "value": int(value) if value.isdigit() else value 
            })

        result = PlayersService.query_dynamic(db, filters=filters, limit=limit)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
