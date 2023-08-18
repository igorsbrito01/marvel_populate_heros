from sqlalchemy import func, select

from comics.models import Character, Comics, CharacterComics
from settings_db import get_db_session


def create_character(id, name, description, picture_url):
    with get_db_session() as session:
        characters = Character(
            id=id, name=name, description=description, picture_url=picture_url
        )
        session.add(characters)
        session.commit()


def get_character_by_id(id):
    with get_db_session() as session:
        character = session.query(Character).filter_by(id=id).first()
        session.expunge_all()
        return character


def get_character_by_name(name):
    with get_db_session() as session:
        character = session.query(Character).filter_by(name=name).first()
        session.expunge_all()
        return character


def if_character_doesnt_exists_create(id, name, description):
    character = get_character_by_id(id)
    if not character:
        create_character(id, name, description)


def create_comics(id, title, description):
    with get_db_session() as session:
        comics = Comics(id=id, title=title, description=description)
        session.add(comics)
        session.commit()


def get_comics_by_id(id):
    with get_db_session() as session:
        comics = session.query(Comics).filter_by(id=id).first()
        session.expunge_all()
        return comics


def if_comics_doesnt_exists_create(id, title, description):
    character = get_comics_by_id(id)
    if not character:
        create_comics(id, title, description)


def create_relation_character_comics(character_id, comics_id):
    with get_db_session() as session:
        character_comics = CharacterComics(
            character_id=character_id, comics_id=comics_id
        )
        session.add(character_comics)
        session.commit()


def check_exists(class_name, id):
    with get_db_session() as session:
        exists = session.query(
            session.query(class_name).filter_by(id=id).exists()
        ).scalar()
        return exists


def check_character_comics(character_id, comics_id):
    with get_db_session() as session:
        exists = session.query(
            session.query(CharacterComics)
            .filter_by(character_id=character_id, comics_id=comics_id)
            .exists()
        ).scalar()
        return exists


def insert_in_bulk(objects):
    with get_db_session() as session:
        session.bulk_save_objects(objects)
        session.commit()


def count_rows(class_name):
    with get_db_session() as session:
        return session.scalar(select(func.count()).select_from(class_name))
