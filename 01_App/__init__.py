from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "fixit-development"
    init_db()
    from .routes import bp
    app.register_blueprint(bp)
    return app
