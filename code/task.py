import logging

from comics.models import Character, Comics, CharacterComics
from comics.services import check_exists, check_character_comics, insert_in_bulk
from marvels_api import (
    get_character_by_name,
    get_comics_from_character_id,
    get_characters_from_comics_id,
)
from utils import build_image_url

logging.basicConfig(
    level=logging.INFO, filename="./logging/character_info.log", filemode="w"
)


def populate_character_and_assosiations(character_name):
    characters_to_save = {}
    comics_to_save = {}
    character_comics_to_save = {}

    status_code, data = get_character_by_name(character_name)

    if not data:
        logging.error("fetch character fail code %s-%s", status_code, character_name)
        return

    main_character = data[0]
    main_id = main_character["id"]

    exists = check_exists(Character, main_id)
    if not exists:
        character = Character(
            id=main_character["id"],
            name=main_character["name"],
            description=main_character["description"],
            picture_url=build_image_url(
                main_character["thumbnail"]["path"],
                main_character["thumbnail"]["extension"],
            ),
        )
        characters_to_save[main_id] = character

    offset = 0
    while offset is not None:
        status_code, data, offset = get_comics_from_character_id(main_id, offset)

        if not data:
            logging.error("comics character fail code %s-%s", status_code, main_id)
            continue

        for comics_data in data:
            comics_id = comics_data["id"]
            exists = check_exists(Comics, comics_id)

            if comics_id not in comics_to_save and not exists:
                comics = Comics(
                    id=comics_data["id"],
                    title=comics_data["title"],
                    description=comics_data["description"],
                )

                comics_to_save[comics_id] = comics

            exists = check_character_comics(main_id, comics_id)
            if (main_id, comics_id) not in character_comics_to_save and not exists:
                character_comics = CharacterComics(
                    character_id=main_id, comics_id=comics_id
                )
                character_comics_to_save[(main_id, comics_id)] = character_comics

            offset_characters = 0
            while offset_characters is not None:
                (
                    status_code,
                    data_character,
                    offset_characters,
                ) = get_characters_from_comics_id(comics_id, offset_characters)

                if not data:
                    logging.error(
                        "comics character fail code %s-%s",
                        status_code,
                        comics_id,
                    )
                    continue

                for data_char in data_character:
                    exists = check_exists(Character, data_char["id"])
                    if data_char["id"] not in characters_to_save and not exists:
                        char_related = Character(
                            id=data_char["id"],
                            name=data_char["name"],
                            description=data_char["description"],
                            picture_url=build_image_url(
                                main_character["thumbnail"]["path"],
                                main_character["thumbnail"]["extension"],
                            ),
                        )
                        characters_to_save[char_related.id] = char_related

                    exists = check_character_comics(data_char["id"], comics_id)
                    if (
                        data_char["id"],
                        comics_id,
                    ) not in character_comics_to_save and not exists:
                        character_comics = CharacterComics(
                            character_id=data_char["id"], comics_id=comics_id
                        )
                        character_comics_to_save[
                            (data_char["id"], comics_id)
                        ] = character_comics

    insert_in_bulk([item for item in characters_to_save.values()])
    insert_in_bulk([item for item in comics_to_save.values()])
    insert_in_bulk([item for item in character_comics_to_save.values()])


populate_character_and_assosiations("Spectrum")
