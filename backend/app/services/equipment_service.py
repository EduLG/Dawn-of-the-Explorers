from app.repositories.equipment_repository import (
    get_equipment_by_type as get_equipment_by_type_repo,
    get_equipment_by_id,
    update_character_equipment as update_character_equipment_repo,
    is_equipment_on_other_character,
)
from app.repositories.character_repository import get_character_by_id
from app.services.auth_service import ServiceError
from app.schemas import EquipmentSchema
from app.models.equipment import JOB_ARMOR_TYPE


def get_equipment_by_type(equipment_type):
    if not equipment_type:
        raise ServiceError("equipment_type is required", 400)

    items = get_equipment_by_type_repo(equipment_type)
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

    job_name = character.current_job.name
    if equipment.equipment_type != JOB_ARMOR_TYPE.get(job_name):
        raise ServiceError("Equipment is not compatible with this character's job", 400)

    if is_equipment_on_other_character(equipment_id, character.party_id, int(character_id)):
        raise ServiceError("This item is already equipped by another character", 409)

    update_character_equipment_repo(character_id, slot, equipment_id)
