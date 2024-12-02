from app.config import create_app
from app.controllers.player_controller import player_blueprint

app = create_app()

# Register Blueprints
app.register_blueprint(player_blueprint, url_prefix='/api/players')

if __name__ == '__main__':
    app.run(debug=True)
