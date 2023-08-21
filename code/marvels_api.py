import requests
from typing import Tuple, Optional, Dict, Any, List

from utils import TS, PUBLIC_KEY, create_api_hash

BASE_URL = "https://gateway.marvel.com"
BASE_URL_CHARACTERS = "/v1/public/characters"
BASE_URL_COMICS = "/v1/public/comics/"


def get_credentials():
    hash = create_api_hash()

    return f"ts={TS}&apikey={PUBLIC_KEY}&hash={hash}"


def build_response_default_single_value(
    status_code: int, content: Dict[str, Any]
) -> Tuple[int, Optional[List[Dict[str, Any]]]]:
    if status_code == 200:
        return status_code, content["data"]["results"]

    return status_code, None


def build_response_default_multiple_values(
    status_code: int, content: Dict[str, Any]
) -> Tuple[int, Optional[List[Dict[str, Any]]], Optional[int]]:
    data = None
    offset_next = None
    if status_code == 200:
        data = content["data"]["results"]
        next = content["data"]["offset"] + content["data"]["limit"] + 1
        if content["data"]["total"] > next:
            offset_next = next

    return status_code, data, offset_next


def get_character_by_name(
    character_name: str,
) -> Tuple[int, Optional[List[Dict[str, Any]]]]:
    credentials = get_credentials()
    url = f"{BASE_URL}{BASE_URL_CHARACTERS}?{credentials}&name={character_name}"

    response = requests.get(url)

    return build_response_default_single_value(response.status_code, response.json())


def get_character_by_id(
    character_id: int,
) -> Tuple[int, Optional[List[Dict[str, Any]]]]:
    credentials = get_credentials()
    url = f"{BASE_URL}{BASE_URL_CHARACTERS}/{character_id}?{credentials}"

    response = requests.get(url)

    return build_response_default_single_value(response.status_code, response.json())


def get_comics_by_id(comics_id: int) -> Tuple[int, Optional[List[Dict[str, Any]]]]:
    credentials = get_credentials()
    url = f"{BASE_URL}{BASE_URL_COMICS}/{comics_id}?{credentials}"

    response = requests.get(url)

    return build_response_default_single_value(response.status_code, response.json())


def get_characters_from_comics_id(
    comics_id: int, offset: int = 0
) -> Tuple[int, Optional[List[Dict[str, Any]]], Optional[int]]:
    credentials = get_credentials()
    url = (
        f"{BASE_URL}{BASE_URL_COMICS}/{comics_id}/"
        f"characters?{credentials}&orderBy=name&offset={offset}"
    )

    response = requests.get(url)

    return build_response_default_multiple_values(response.status_code, response.json())


def get_comics_from_character_id(
    character_id: int, offset: int = 0
) -> Tuple[int, Optional[List[Dict[str, Any]]], Optional[int]]:
    credentials = get_credentials()
    url = (
        f"{BASE_URL}{BASE_URL_CHARACTERS}/{character_id}/"
        f"comics?{credentials}&orderBy=title&offset={offset}"
    )

    response = requests.get(url)

    return build_response_default_multiple_values(response.status_code, response.json())
