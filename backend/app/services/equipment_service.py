from app.repositories.equipment_repository import get_equipment_by_type as get_equipment_by_type_repo
from app.services.auth_service import ServiceError
from app.schemas import EquipmentSchema


def get_equipment_by_type(equipment_type):
    if not equipment_type:
        raise ServiceError("equipment_type is required", 400)

    items = get_equipment_by_type_repo(equipment_type)
    return EquipmentSchema(many=True).dump(items)
