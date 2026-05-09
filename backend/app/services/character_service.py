from typing import Iterable

from app.repositories.character_repository import get_character_by_id


def calculate_character_rating(equipment_relations: Iterable) -> int:
    total = 0
    for relation in equipment_relations or []:
        equipment = getattr(relation, "equipment", None)
        total += getattr(equipment, "rating", 0) or 0
    return total
