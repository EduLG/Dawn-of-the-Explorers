from app.models.character import Character


def get_character_by_id(character_id):
    return Character.query.filter_by(id=character_id).first()
