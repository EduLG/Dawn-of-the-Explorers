from app.models.equipment import Equipment


def get_equipment_by_job(job_id):
    return Equipment.query.filter_by(job_id=job_id).all()
