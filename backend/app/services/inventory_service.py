from app.models.user import User
from app.repositories.inventory_repository import (
    get_party_inventory,
    get_inventory_item,
    remove_from_inventory,
)
from app.repositories.equipment_repository import update_character_equipment as update_char_equip_repo
from app.repositories.character_repository import get_character_by_id
from app.services.auth_service import ServiceError
from app.schemas import PartyInventorySchema


def get_inventory(user_id):
    user = User.query.get(user_id)
    if not user or not user.party:
        raise ServiceError("Party not found", 404)

    items = get_party_inventory(user.party.id)
    return PartyInventorySchema(many=True).dump(items)


def equip_from_inventory(user_id, inventory_id, character_id, slot):
    user = User.query.get(user_id)
    if not user or not user.party:
        raise ServiceError("Party not found", 404)

    inventory_item = get_inventory_item(inventory_id)
    if not inventory_item:
        raise ServiceError("Inventory item not found", 404)

    if inventory_item.party_id != user.party.id:
        raise ServiceError("Forbidden", 403)

    character = get_character_by_id(character_id)
    if not character or character.party_id != user.party.id:
        raise ServiceError("Character not found", 404)

    equipment = inventory_item.equipment
    if equipment.job_id != character.current_job_id:
        raise ServiceError("Equipment is not compatible with this character's job", 400)

    update_char_equip_repo(character_id, slot, equipment.id)
    remove_from_inventory(inventory_id)
