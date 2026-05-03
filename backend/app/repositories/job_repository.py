from app.models.job import Job


def get_all_jobs():
    return Job.query.order_by(Job.id).all()
