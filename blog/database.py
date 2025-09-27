from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlAlchmeyUrl = 'sqlite:///./blog.db'
engine = create_engine(sqlAlchmeyUrl, connect_args={
    'check_same_thread':False
})

localSession = sessionmaker(bind=engine, autocommit = False,autoflush=False,)

base = declarative_base()