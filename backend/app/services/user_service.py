from app.repositories.user_repository import get_user_by_id
from app.services.auth_service import ServiceError


def get_user_profile(user_id):
	user = get_user_by_id(user_id)
	if not user:
		raise ServiceError("User not found", 404)

	# basic serialization: user fields and party info with characters
	result = {
		"id": user.id,
		"username": user.username,
		"email": user.email,
		"party": None,
	}

	if user.party:
		party = user.party
		characters = []
		for entry in party.characters:
			ch = getattr(entry, "character", entry)
			characters.append({
				"id": ch.id,
				"name": ch.name,
				"party_slot": getattr(entry, "party_slot", None),
			})

		result["party"] = {
			"id": party.id,
			"name": party.name,
			"level": party.level,
			"experience": party.experience,
			"rating": party.rating,
			"characters": characters,
		}

	return result
