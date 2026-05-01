import random

from app.models.user import User
from app.models.equipment import Equipment
from app.repositories.dungeon_repository import get_dungeon_by_id, get_visible_dungeons
from app.repositories.inventory_repository import add_to_inventory
from app.services.auth_service import ServiceError
from app.services.party_service import calculate_party_rating
from app.schemas.dungeon_schema import DungeonSchema
from app.schemas.equipment_schema import EquipmentSchema


def get_dungeons(user_id):
    user = User.query.get(user_id)
    if not user or not user.party:
        raise ServiceError("Party not found", 404)

    party_rating = calculate_party_rating(user.party.characters)
    dungeons = get_visible_dungeons(party_rating)
    return DungeonSchema(many=True).dump(dungeons)


def explore_dungeon(user_id, dungeon_id):
    user = User.query.get(user_id)
    if not user or not user.party:
        raise ServiceError("Party not found", 404)

    dungeon = get_dungeon_by_id(dungeon_id)
    if not dungeon:
        raise ServiceError("Dungeon not found", 404)

    party_rating = calculate_party_rating(user.party.characters)

    if party_rating < dungeon.visibility_rating:
        raise ServiceError("Dungeon not yet discovered", 403)

    success, n_items = _resolve(party_rating, dungeon.min_rating)

    if not success:
        return {"success": False, "loot": []}

    loot_ids = dungeon.loot or []
    sample_ids = random.sample(loot_ids, min(n_items, len(loot_ids)))
    items = Equipment.query.filter(Equipment.id.in_(sample_ids)).all()

    for item in items:
        add_to_inventory(user.party.id, item.id)

    return {
        "success": True,
        "loot": EquipmentSchema(many=True).dump(items),
    }


def _resolve(party_rating, min_rating):
    if min_rating == 0:
        return True, 5

    ratio = party_rating / min_rating

    if ratio < 0.5:
        prob, n_items = 0.10, 1
    elif ratio < 0.8:
        prob, n_items = 0.40, 2
    elif ratio < 1.0:
        prob, n_items = 0.70, 3
    elif ratio <= 1.3:
        prob, n_items = 0.90, 4
    else:
        prob, n_items = 0.99, 6

    return random.random() < prob, n_items
