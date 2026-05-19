from flask import Flask
from src.repo.database import Database
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.Config")

    db = Database().db
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def homepage():
        return "Welcome to Nkata Blog Application"

    from src.controllers.user_controller import user_bp
    from src.controllers.post_controller import post_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    @app.cli.command("create_db")
    def create_db():
        db.create_all()
        print("Database created")

    return app