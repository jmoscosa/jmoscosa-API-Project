from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


# This creates the table class
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title_of_post = Column(String(20), nullable=False)
    content = Column(String(20), nullable=False)  # <-had to add the length allowed of the strings for mysql to work
    published = Column(Boolean, server_default=text('0'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Here we are going to reference a value from a different table BUT it is not a foregin key
    owner = relationship("User")


# This creates the user class
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# This creates the table for "likes"
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="Cascade"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="Cascade"), primary_key=True)
