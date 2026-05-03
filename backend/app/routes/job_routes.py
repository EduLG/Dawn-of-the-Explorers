from flask import Blueprint
from app.handlers.job_handler import get_jobs_handler

job_bp = Blueprint("jobs", __name__)

job_bp.route("", methods=["GET"])(get_jobs_handler)
