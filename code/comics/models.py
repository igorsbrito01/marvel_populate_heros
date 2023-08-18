from sqlalchemy import Integer, ForeignKey, String, Text
from sqlalchemy.orm import mapped_column, relationship

from utils_db import Base


class Character(Base):
    __tablename__ = "character"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(120), nullable=False)
    description = mapped_column(Text(5000), nullable=True)
    picture_url = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"Characters {self.name}"


class Comics(Base):
    __tablename__ = "comics"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(120), nullable=False)
    description = mapped_column(Text(5000), nullable=True)


class CharacterComics(Base):
    __tablename__ = "character_comics"

    character_id = mapped_column(Integer, ForeignKey("character.id"), primary_key=True)
    comics_id = mapped_column(Integer, ForeignKey("comics.id"), primary_key=True)

    character = relationship(Character, backref="set_characters")
    comics = relationship(Comics, backref="set_comics")
