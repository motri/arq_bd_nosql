from flask import Blueprint, request, jsonify
from app.services.player_service import transform_player_data
from app.repositories.player_repository import insert_players, query_best_players

player_blueprint = Blueprint('player_controller', __name__)

@player_blueprint.route('/players/load', methods=['POST'])
def load_players():
    data = request.json  # Assumes JSON data is sent in POST request
    transformed_data = transform_player_data(data)
    db = request.app.config['MONGO_DB']
    insert_players(db, transformed_data)
    return jsonify({"message": "Players inserted successfully!"}), 201

@player_blueprint.route('/players/top', methods=['GET'])
def get_top_players():
    age = int(request.args.get('age', 21))
    field = request.args.get('field', 'goals')
    limit = int(request.args.get('limit', 10))
    db = request.app.config['MONGO_DB']
    
    # Get the data and metrics
    result = query_best_players(db, age, field, limit)
    players = result["data"]
    execution_time = result["execution_time"]
    
    # Include metrics in the response
    return jsonify({
        "data": players,
        "metrics": {
            "execution_time": execution_time,
            "query_params": {
                "age_threshold": age,
                "sort_field": field,
                "limit": limit
            }
        }
    }), 200
