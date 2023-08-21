import hashlib
from settings import TS, PRIVATE_KEY, PUBLIC_KEY


def create_api_hash() -> str:
    hashable_str = f"{TS}{PRIVATE_KEY}{PUBLIC_KEY}"
    return hashlib.md5(hashable_str.encode("utf-8")).hexdigest()


def build_image_url(path: str, extention: str) -> str:
    return f"{path}.{extention}"
