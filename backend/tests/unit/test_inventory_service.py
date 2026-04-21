import pytest
from app.services.inventory_service import get_inventory, equip_from_inventory, ServiceError


class TestGetInventory:

    def test_user_without_party_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party = None
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        with pytest.raises(ServiceError) as exc_info:
            get_inventory(user_id=1)

        assert exc_info.value.status_code == 404

    def test_valid_user_returns_serialized_list(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        fake_items = [mocker.Mock(), mocker.Mock()]
        mocker.patch("app.services.inventory_service.get_party_inventory", return_value=fake_items)

        fake_schema = mocker.Mock()
        fake_schema.dump.return_value = [{"id": 1}, {"id": 2}]
        mocker.patch("app.services.inventory_service.PartyInventorySchema", return_value=fake_schema)

        result = get_inventory(user_id=1)

        assert result == [{"id": 1}, {"id": 2}]
        fake_schema.dump.assert_called_once_with(fake_items)


class TestEquipFromInventory:

    def test_user_without_party_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party = None
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 404

    def test_inventory_item_not_found_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=99, character_id=1, slot="head")

        assert exc_info.value.status_code == 404

    def test_item_from_other_party_raises_403(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        fake_item = mocker.Mock()
        fake_item.party_id = 2
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 403

    def test_character_from_other_party_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        fake_character = mocker.Mock()
        fake_character.party_id = 2
        mocker.patch("app.services.inventory_service.get_character_by_id", return_value=fake_character)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 404

    def test_incompatible_job_raises_400(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        fake_item.equipment.job_id = 2
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        fake_character = mocker.Mock()
        fake_character.party_id = 1
        fake_character.current_job_id = 1
        mocker.patch("app.services.inventory_service.get_character_by_id", return_value=fake_character)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 400

    def test_valid_data_equips_and_removes_from_inventory(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mocker.patch("app.services.inventory_service.User.query.get", return_value=fake_user)

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        fake_item.equipment.job_id = 1
        fake_item.equipment.id = 5
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        fake_character = mocker.Mock()
        fake_character.party_id = 1
        fake_character.current_job_id = 1
        mocker.patch("app.services.inventory_service.get_character_by_id", return_value=fake_character)

        mock_update = mocker.patch("app.services.inventory_service.update_char_equip_repo")
        mock_remove = mocker.patch("app.services.inventory_service.remove_from_inventory")

        equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        mock_update.assert_called_once_with(1, "head", 5)
        mock_remove.assert_called_once_with(1)
