from typing import Iterable

from app.repositories.character_repository import (
    get_character_by_id,
    update_character_job,
    unequip_all,
)
from app.repositories.job_repository import get_job_by_id
from app.services.auth_service import ServiceError


def calculate_character_rating(equipment_relations: Iterable) -> int:
    total = 0
    for relation in equipment_relations or []:
        equipment = getattr(relation, "equipment", None)
        total += getattr(equipment, "rating", 0) or 0
    return total


def change_character_job(user_id, character_id, job_id):
    character = get_character_by_id(character_id)
    if not character:
        raise ServiceError("Character not found", 404)
    if character.party.user.id != user_id:
        raise ServiceError("Forbidden", 403)

    job = get_job_by_id(job_id)
    if not job:
        raise ServiceError("Job not found", 404)

    unequip_all(character_id)
    update_character_job(character_id, job_id)

