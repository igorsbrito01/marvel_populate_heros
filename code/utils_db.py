from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import DB_CONN_STR


# "mysql+mysqlconnector://marvel_user:20101020@ulocalhost:3306/marvel_comics",
engine = create_engine(DB_CONN_STR, echo=True)

Base = declarative_base()


def get_db_session():
    Session = sessionmaker(bind=engine)
    return Session()


def create_all_tables():
    from comics.models import CharacterComics, Character, Comics

    Base.metadata.create_all(engine)


def drop_tables():
    from comics.models import CharacterComics, Character, Comics

    CharacterComics.__table__.drop(engine)
    Character.__table__.drop(engine)
    Comics.__table__.drop(engine)
