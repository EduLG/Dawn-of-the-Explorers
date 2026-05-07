import pytest
from app.services.auth_service import register_user, authenticate_user, ServiceError


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


class TestAuthenticateUser:

    def test_authenticate_valid_credentials_returns_tokens(self, mocker):
        fake_user = mocker.Mock()
        fake_user.id = 1
        fake_user.username = "eduladron"
        mocker.patch("app.services.auth_service.get_user_by_username", return_value=fake_user)
        mocker.patch("app.services.auth_service.check_password_hash", return_value=True)
        mocker.patch("app.services.auth_service.create_access_token", return_value="fake_access")
        mocker.patch("app.services.auth_service.create_refresh_token", return_value="fake_refresh")

        result = authenticate_user("eduladron", "securepass")

        assert result["access_token"] == "fake_access"
        assert result["refresh_token"] == "fake_refresh"
        assert result["user_id"] == 1
        assert result["username"] == "eduladron"

    def test_authenticate_missing_data_raises_400(self):
        with pytest.raises(ServiceError) as exc_info:
            authenticate_user("", "")

        assert exc_info.value.status_code == 400

    def test_authenticate_unknown_username_raises_401(self, mocker):
        mocker.patch("app.services.auth_service.get_user_by_username", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            authenticate_user("fantasma", "securepass")

        assert exc_info.value.status_code == 401

    def test_authenticate_wrong_password_raises_401(self, mocker):
        fake_user = mocker.Mock()
        mocker.patch("app.services.auth_service.get_user_by_username", return_value=fake_user)
        mocker.patch("app.services.auth_service.check_password_hash", return_value=False)

        with pytest.raises(ServiceError) as exc_info:
            authenticate_user("eduladron", "wrongpass")

        assert exc_info.value.status_code == 401
