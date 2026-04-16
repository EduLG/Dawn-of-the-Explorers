from app.repositories.equipment_repository import get_equipment_by_job as get_equipment_by_job_repo
from app.services.auth_service import ServiceError
from app.schemas import EquipmentSchema


def get_equipment_by_job(job_id):
    if not job_id:
        raise ServiceError("job_id is required", 400)

    items = get_equipment_by_job_repo(job_id)
    return EquipmentSchema(many=True).dump(items)
