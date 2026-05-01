from app.models.dungeon import Dungeon


def get_dungeon_by_id(dungeon_id):
    return Dungeon.query.get(dungeon_id)


def get_visible_dungeons(party_rating):
    return (
        Dungeon.query
        .filter(Dungeon.visibility_rating <= party_rating)
        .order_by(Dungeon.min_rating)
        .all()
    )
