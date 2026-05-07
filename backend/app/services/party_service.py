from typing import Iterable
from app.services.character_service import calculate_character_rating

def calculate_party_rating(characters: Iterable) -> int:
    total=0
    for character in characters or []:
        total += calculate_character_rating(getattr(character, "equipment", []))
    return total