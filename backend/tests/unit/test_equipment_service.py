import pytest
from app.services.equipment_service import get_equipment_by_job, update_character_equipment, ServiceError


class TestGetEquipmentByJob:

    def test_missing_job_id_raises_400(self):
        with pytest.raises(ServiceError) as exc_info:
            get_equipment_by_job(None)

        assert exc_info.value.status_code == 400

    def test_valid_job_id_returns_serialized_list(self, mocker):
        fake_items = [mocker.Mock(), mocker.Mock()]
        mocker.patch("app.services.equipment_service.get_equipment_by_job_repo", return_value=fake_items)

        fake_schema = mocker.Mock()
        fake_schema.dump.return_value = [{"id": 1}, {"id": 2}]
        mocker.patch("app.services.equipment_service.EquipmentSchema", return_value=fake_schema)

        result = get_equipment_by_job(job_id=3)

        assert result == [{"id": 1}, {"id": 2}]
        fake_schema.dump.assert_called_once_with(fake_items)


class TestUpdateCharacterEquipment:

    def test_character_not_found_raises_404(self, mocker):
        mocker.patch("app.services.equipment_service.get_character_by_id", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            update_character_equipment(user_id=1, character_id=99, slot="head", equipment_id=1)

        assert exc_info.value.status_code == 404

    def test_character_belongs_to_other_user_raises_403(self, mocker):
        fake_character = mocker.Mock()
        fake_character.party.user.id = 2
        mocker.patch("app.services.equipment_service.get_character_by_id", return_value=fake_character)

        with pytest.raises(ServiceError) as exc_info:
            update_character_equipment(user_id=1, character_id=1, slot="head", equipment_id=1)

        assert exc_info.value.status_code == 403

    def test_equipment_not_found_raises_404(self, mocker):
        fake_character = mocker.Mock()
        fake_character.party.user.id = 1
        mocker.patch("app.services.equipment_service.get_character_by_id", return_value=fake_character)
        mocker.patch("app.services.equipment_service.get_equipment_by_id", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            update_character_equipment(user_id=1, character_id=1, slot="head", equipment_id=99)

        assert exc_info.value.status_code == 404

    def test_incompatible_job_raises_400(self, mocker):
        fake_character = mocker.Mock()
        fake_character.party.user.id = 1
        fake_character.current_job_id = 1
        mocker.patch("app.services.equipment_service.get_character_by_id", return_value=fake_character)

        fake_equipment = mocker.Mock()
        fake_equipment.job_id = 2
        mocker.patch("app.services.equipment_service.get_equipment_by_id", return_value=fake_equipment)

        with pytest.raises(ServiceError) as exc_info:
            update_character_equipment(user_id=1, character_id=1, slot="head", equipment_id=1)

        assert exc_info.value.status_code == 400

    def test_valid_data_calls_repository(self, mocker):
        fake_character = mocker.Mock()
        fake_character.party.user.id = 1
        fake_character.current_job_id = 1
        mocker.patch("app.services.equipment_service.get_character_by_id", return_value=fake_character)

        fake_equipment = mocker.Mock()
        fake_equipment.job_id = 1
        mocker.patch("app.services.equipment_service.get_equipment_by_id", return_value=fake_equipment)

        mock_repo = mocker.patch("app.services.equipment_service.update_character_equipment_repo")

        update_character_equipment(user_id=1, character_id=1, slot="head", equipment_id=1)

        mock_repo.assert_called_once_with(1, "head", 1)
