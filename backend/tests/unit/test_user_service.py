import pytest
from app.services.user_service import get_user_profile, ServiceError


class TestGetUserProfile:

    def test_user_not_found_raises_404(self, mocker):
        mocker.patch("app.services.user_service.get_user_by_id", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            get_user_profile(user_id=99)

        assert exc_info.value.status_code == 404

    def test_valid_user_returns_serialized_profile(self, mocker):
        fake_user = mocker.Mock()
        mocker.patch("app.services.user_service.get_user_by_id", return_value=fake_user)

        fake_schema = mocker.Mock()
        fake_schema.dump.return_value = {"id": 1, "username": "eduladron"}
        mocker.patch("app.services.user_service.UserSchema", return_value=fake_schema)

        result = get_user_profile(user_id=1)

        assert result == {"id": 1, "username": "eduladron"}
        fake_schema.dump.assert_called_once_with(fake_user)
