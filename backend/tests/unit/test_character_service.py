from app.services.character_service import calculate_character_rating


class TestCalculateCharacterRating:

    def test_empty_list_returns_zero(self):
        result = calculate_character_rating([])

        assert result == 0
