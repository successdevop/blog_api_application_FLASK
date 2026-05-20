import secrets

from sqlalchemy.orm import relationship

from src.repo.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime


class Comments(db.Model):
    __tablename__ = "comments"
    comment_id = Column(String(20), primary_key=True, default=lambda : secrets.token_hex(10))
    body = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
