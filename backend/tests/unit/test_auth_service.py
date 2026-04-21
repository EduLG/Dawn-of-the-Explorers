import pytest
from app.services.auth_service import register_user, ServiceError


class TestRegisterUser:

    def test_register_valid_data_creates_user(self, mocker):
        # --- Arrange ---
        # Sustituimos las funciones que hablan con la BD por versiones falsas.
        # return_value=None simula que el usuario NO existe todavia (sin duplicados).
        mocker.patch("app.services.auth_service.get_user_by_username", return_value=None)
        mocker.patch("app.services.auth_service.get_user_by_email", return_value=None)

        # create_user es la llamada final que "guarda" el usuario.
        # Le decimos que devuelva un objeto falso con un atributo id=1.
        fake_user = mocker.Mock()
        fake_user.id = 1
        mock_create = mocker.patch("app.services.auth_service.create_user", return_value=fake_user)

        # --- Act ---
        result = register_user("eduladron", "edu@test.com", "securepass")

        # --- Assert ---
        # El resultado debe ser el usuario falso que devolvio create_user
        assert result == fake_user

        # create_user debe haberse llamado exactamente una vez, con username y email correctos.
        # No comprobamos el password porque el service lo hashea antes de pasarlo.
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        assert call_args[0][0] == "eduladron"
        assert call_args[0][1] == "edu@test.com"
