from flask import Flask
from src.repo.database import Database

def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.Config")

    db = Database().db
    db.init_app(app)

    from src.controllers.user_controller import app_bp
    app.register_blueprint(app_bp)


    @app.cli.command("created_db")
    def created_db():
        db.create_all()
        print("Database created")

    return app