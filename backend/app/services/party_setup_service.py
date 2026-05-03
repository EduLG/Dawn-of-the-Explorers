from app.models.user import User
from app.models.character import Character
from app.models.job import Job
from app.services.auth_service import ServiceError
from app.extensions import db


def setup_party(user_id, party_name, characters_data):
    user = User.query.get(user_id)
    if not user or not user.party:
        raise ServiceError("Party not found", 404)

    if len(user.party.characters) > 0:
        raise ServiceError("Party already set up", 409)

    party_name = party_name.strip() if party_name else ""
    if not party_name:
        raise ServiceError("Party name is required", 400)

    if len(characters_data) != 4:
        raise ServiceError("Exactly 4 characters are required", 400)

    for char_data in characters_data:
        name = (char_data.get("name") or "").strip()
        job_id = char_data.get("job_id")

        if not name:
            raise ServiceError("All characters must have a name", 400)

        if not job_id:
            raise ServiceError("All characters must have a job", 400)

        job = Job.query.get(job_id)
        if not job:
            raise ServiceError(f"Job {job_id} not found", 404)

        character = Character(
            name=name,
            party_id=user.party.id,
            current_job_id=job_id,
        )
        db.session.add(character)

    user.party.name = party_name
    db.session.commit()
