from .database import base
from sqlalchemy import INTEGER, Column, String

class Blog(base):
    __tablename__ = "blogUsers"
    id = Column(INTEGER, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

class User(base):
    __tablename__ = "Users"
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String)
    mail = Column(String)
    password = Column(String)