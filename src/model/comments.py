from sqlalchemy.orm import relationship

from src.repo.database import Database
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime


class Comments(Database.db.Model):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey("users.user_id"))
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    user = relationship("User", back_populates="comments")