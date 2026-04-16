from app.repositories.equipment_repository import (
    get_equipment_by_job as get_equipment_by_job_repo,
    get_equipment_by_id,
    update_character_equipment as update_character_equipment_repo,
)
from app.repositories.character_repository import get_character_by_id
from app.services.auth_service import ServiceError
from app.schemas import EquipmentSchema


def get_equipment_by_job(job_id):
    if not job_id:
        raise ServiceError("job_id is required", 400)

    items = get_equipment_by_job_repo(job_id)
    return EquipmentSchema(many=True).dump(items)


def update_character_equipment(user_id, character_id, slot, equipment_id):
    character = get_character_by_id(character_id)
    if not character:
        raise ServiceError("Character not found", 404)

    if character.party.user.id != user_id:
        raise ServiceError("Forbidden", 403)

    equipment = get_equipment_by_id(equipment_id)
    if not equipment:
        raise ServiceError("Equipment not found", 404)

    if equipment.job_id != character.current_job_id:
        raise ServiceError("Equipment is not compatible with this character's job", 400)

    update_character_equipment_repo(character_id, slot, equipment_id)
