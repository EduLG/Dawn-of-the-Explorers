from app.models.job import Job


def get_all_jobs():
    return Job.query.order_by(Job.id).all()


def get_job_by_id(job_id):
    return Job.query.filter_by(id=job_id).first()
