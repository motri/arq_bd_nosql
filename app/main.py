from config import create_app
from controllers import players_blueprint, teams_blueprint, goalkeepers_blueprint

app = create_app()

# Register Blueprints
app.register_blueprint(players_blueprint, url_prefix='/api/players')
app.register_blueprint(teams_blueprint, url_prefix='/api/teams')
app.register_blueprint(goalkeepers_blueprint, url_prefix='/api/goalkeepers')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

