from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.model.comments import Comments


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comments
        load_instance = True
        include_fk = True
        fields = ("comment_id", "body", "timestamp", "author_id", "post_id")


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)