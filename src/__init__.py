from flask import Flask
from config import Config
from src.repo.database import Database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Database.db.init_app(app)

    return app