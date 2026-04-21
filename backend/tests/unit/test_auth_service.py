import pytest
from app.services.auth_service import register_user, ServiceError


class TestRegisterUser:

    def test_register_valid_data_creates_user(self, mocker):

        mocker.patch("app.services.auth_service.get_user_by_username", return_value=None)
        mocker.patch("app.services.auth_service.get_user_by_email", return_value=None)

        fake_user = mocker.Mock()
        fake_user.id = 1
        mock_create = mocker.patch("app.services.auth_service.create_user", return_value=fake_user)

        result = register_user("eduladron", "edu@test.com", "securepass")

        assert result == fake_user

        mock_create.assert_called_once()
        call_args = mock_create.call_args
        assert call_args[0][0] == "eduladron"
        assert call_args[0][1] == "edu@test.com"

    def test_register_missing_data_raises_400(self):
        with pytest.raises(ServiceError) as exc_info:
            register_user("", "", "")

        assert exc_info.value.status_code == 400

    def test_register_duplicate_username_raises_409(self, mocker):
        mocker.patch("app.services.auth_service.get_user_by_username", return_value=mocker.Mock())
        mocker.patch("app.services.auth_service.get_user_by_email", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            register_user("eduladron", "edu@test.com", "securepass")

        assert exc_info.value.status_code == 409

    def test_register_duplicate_email_raises_409(self, mocker):
        mocker.patch("app.services.auth_service.get_user_by_username", return_value=None)
        mocker.patch("app.services.auth_service.get_user_by_email", return_value=mocker.Mock())

        with pytest.raises(ServiceError) as exc_info:
            register_user("eduladron", "edu@test.com", "securepass")

        assert exc_info.value.status_code == 409
