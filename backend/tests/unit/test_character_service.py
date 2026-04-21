from types import SimpleNamespace
from app.services.character_service import calculate_character_rating


class TestCalculateCharacterRating:

    def test_empty_list_returns_zero(self):
        result = calculate_character_rating([])

        assert result == 0

    def test_sums_all_equipment_ratings(self):
        relations = [
            SimpleNamespace(equipment=SimpleNamespace(rating=10)),
            SimpleNamespace(equipment=SimpleNamespace(rating=25)),
            SimpleNamespace(equipment=SimpleNamespace(rating=5)),
        ]

        result = calculate_character_rating(relations)

        assert result == 40
