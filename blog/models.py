from .database import base
from sqlalchemy import INTEGER, Column, ForeignKey, String
from sqlalchemy.orm import relationship

class Blog(base):
    __tablename__ = "blogUsers"
    id = Column(INTEGER, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(INTEGER, ForeignKey("Users.id"))
    creator = relationship("User", back_populates="blog")

class User(base):
    __tablename__ = "Users"
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String)
    mail = Column(String)
    password = Column(String)
    blog = relationship("Blog", back_populates="creator") 