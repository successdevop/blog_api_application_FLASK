from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.model.user import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("user_id", "user_name", "email", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)