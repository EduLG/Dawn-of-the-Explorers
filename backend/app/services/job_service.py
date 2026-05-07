from app.repositories.job_repository import get_all_jobs
from app.schemas.job_schema import JobSchema


def get_jobs():
    return JobSchema(many=True).dump(get_all_jobs())
