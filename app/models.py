from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base): # extends sqlalchemy class
    __tablename__ = "posts" 

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column( TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User") # sqlalchemy: fetches User class for given post

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column( TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text("now()"))
    phone_number = Column(String, )

class Vote(Base):
    """
    To enforce that a user cannot like a post more than once -> composite key (primary key across multiple columns)
    To do this just set both columns as primary keys
    """
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
