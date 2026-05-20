from sqlalchemy.orm import relationship

from src.repo.database import db
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"
    post_id = Column(String, primary_key=True)
    title = Column(String(140), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    author_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="post", lazy="dynamic", cascade="all, delete-orphan")