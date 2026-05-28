from flask import Flask
from src.config import Config

def create_app(config_class=Config):
    """Application factory for initializing the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register routes blueprint
    from src.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
