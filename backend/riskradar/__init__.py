import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        PORT=int(os.getenv("PORT", "5001")),
        ALLOWED_ORIGINS=os.getenv("ALLOWED_ORIGINS", "*"),
    )
    CORS(app, resources={r"/*": {"origins": app.config["ALLOWED_ORIGINS"].split(",")}})

    # Register blueprints
    from .routes.health import bp as health_bp
    from .routes.risks import bp as risks_bp

    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(risks_bp, url_prefix="/api/risks")

    return app


