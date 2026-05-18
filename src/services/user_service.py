from flask import request, jsonify
from src.model.user import User


class UserService:
    def __init__(self, database):
        self._db = database


