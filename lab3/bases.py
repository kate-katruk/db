from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from config import config

Base = declarative_base()
engine = create_engine(f'postgresql://postgres:12316c@localhost/library')
session = sessionmaker(bind=engine)()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)