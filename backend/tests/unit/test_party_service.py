from types import SimpleNamespace
from app.services.party_service import calculate_party_rating


class TestCalculatePartyRating:

    def test_empty_list_returns_zero(self):
        result = calculate_party_rating([])

        assert result == 0

    def test_sums_rating_of_all_characters(self):
        characters = [
            SimpleNamespace(equipment=[
                SimpleNamespace(equipment=SimpleNamespace(rating=10)),
                SimpleNamespace(equipment=SimpleNamespace(rating=20)),
            ]),
            SimpleNamespace(equipment=[
                SimpleNamespace(equipment=SimpleNamespace(rating=5)),
            ]),
        ]

        result = calculate_party_rating(characters)

        assert result == 35

    def test_characters_with_no_equipment_return_zero(self):
        characters = [
            SimpleNamespace(equipment=[]),
            SimpleNamespace(equipment=[]),
        ]

        result = calculate_party_rating(characters)

        assert result == 0
