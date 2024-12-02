from app.config import create_app
from app.controllers.players_controller import players_blueprint
from app.controllers.teams_controller import teams_blueprint
from app.controllers.goalkeepers_controller import goalkeepers_blueprint

app = create_app()

# Register Blueprints
app.register_blueprint(players_blueprint, url_prefix='/api/players')
app.register_blueprint(teams_blueprint, url_prefix='/api/teams')
app.register_blueprint(goalkeepers_blueprint, url_prefix='/api/goalkeepers')

if __name__ == '__main__':
    app.run(debug=True)
