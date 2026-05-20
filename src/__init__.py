from flask import Flask
from src.repo.database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.Config")

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    from src.model import User, Post, Comments

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

    @app.cli.command("drop_db")
    def drop_db():
        db.drop_all()
        print("Database dropped")

    return app