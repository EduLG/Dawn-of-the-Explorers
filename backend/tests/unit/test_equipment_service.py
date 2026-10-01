import pytest
from app.services.equipment_service import get_equipment_by_type, ServiceError


class TestGetEquipmentByType:

    def test_missing_equipment_type_raises_400(self):
        with pytest.raises(ServiceError) as exc_info:
            get_equipment_by_type(None)

        assert exc_info.value.status_code == 400

    def test_valid_equipment_type_returns_serialized_list(self, mocker):
        fake_items = [mocker.Mock(), mocker.Mock()]
        mock_repo = mocker.patch("app.services.equipment_service.get_equipment_by_type_repo", return_value=fake_items)

        fake_schema = mocker.Mock()
        fake_schema.dump.return_value = [{"id": 1}, {"id": 2}]
        mocker.patch("app.services.equipment_service.EquipmentSchema", return_value=fake_schema)

        result = get_equipment_by_type("plate")

        assert result == [{"id": 1}, {"id": 2}]
        mock_repo.assert_called_once_with("plate")
        fake_schema.dump.assert_called_once_with(fake_items)
