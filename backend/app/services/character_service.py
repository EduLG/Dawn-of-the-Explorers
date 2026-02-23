from typing import Iterable


def calculate_character_rating(equipment_relations: Iterable) -> int:
    total=0
    for relation in equipment_relations or []:
        equipment = getattr(relation, "equipment", None)
        total += getattr(equipment, "rating", 0) or 0
    return total

