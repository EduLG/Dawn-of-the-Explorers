from app.repositories.user_repository import get_user_by_id
from app.services.auth_service import ServiceError
from app.services.party_service import calculate_party_rating
from app.services.character_service import calculate_character_rating


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
        party_rating = calculate_party_rating(party.characters)

        for ch in party.characters:
            current_job = None
            if ch.current_job:
                current_job = {
                    "id": ch.current_job.id,
                    "name": ch.current_job.name,
                    "icon": ch.current_job.icon,
                }

            equipped_items = []
            for relation in ch.equipment:
                equipment = relation.equipment
                equipped_items.append(
                    {
                        "slot": relation.slot,
                        "equipment": {
                            "id": equipment.id,
                            "name": equipment.name,
                            "type": equipment.type,
                            "rating": equipment.rating,
                        },
                    }
                )

            characters.append(
                {
                    "id": ch.id,
                    "name": ch.name,
                    "current_job": current_job,
                    "equipped_items": equipped_items,
                    "rating": calculate_character_rating(ch.equipment),
                }
            )

        result["party"] = {
            "id": party.id,
            "name": party.name,
            "level": party.level,
            "experience": party.experience,
            "rating": party_rating,
            "characters": characters,
        }

    return result