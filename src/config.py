import secrets


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///fashion_biz.db?journal_mode=WAL&timeout=30"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secrets.token_hex(32)