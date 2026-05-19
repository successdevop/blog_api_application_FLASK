from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.model.post import Post


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_fk = True
        fields = ("post_id", "title", "body", "created_at", "author_id")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)