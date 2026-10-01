import pytest
from app.services.inventory_service import get_inventory, equip_from_inventory, ServiceError


class TestGetInventory:

    def test_user_without_party_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party = None
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        with pytest.raises(ServiceError) as exc_info:
            get_inventory(user_id=1)

        assert exc_info.value.status_code == 404

    def test_valid_user_returns_serialized_list(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

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
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 404

    def test_inventory_item_not_found_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=None)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=99, character_id=1, slot="head")

        assert exc_info.value.status_code == 404

    def test_item_owned_by_other_user_raises_403(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        fake_item = mocker.Mock()
        fake_item.party_id = 2
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 403

    def test_item_already_equipped_raises_409(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        fake_item.character_equipment = mocker.Mock()
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        mock_update = mocker.patch("app.services.inventory_service.update_char_equip_repo")

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 409
        mock_update.assert_not_called()

    def test_character_owned_by_other_user_raises_404(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        fake_item.character_equipment = None
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
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        fake_item.character_equipment = None
        fake_item.equipment.equipment_type = "plate"
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        fake_character = mocker.Mock()
        fake_character.party_id = 1
        fake_character.current_job.name = "sage"
        mocker.patch("app.services.inventory_service.get_character_by_id", return_value=fake_character)

        mock_update = mocker.patch("app.services.inventory_service.update_char_equip_repo")

        with pytest.raises(ServiceError) as exc_info:
            equip_from_inventory(user_id=1, inventory_id=1, character_id=1, slot="head")

        assert exc_info.value.status_code == 400
        mock_update.assert_not_called()

    def test_valid_data_equips_item(self, mocker):
        fake_user = mocker.Mock()
        fake_user.party.id = 1
        mock_user_class = mocker.patch("app.services.inventory_service.User")
        mock_user_class.query.get.return_value = fake_user

        fake_item = mocker.Mock()
        fake_item.party_id = 1
        fake_item.character_equipment = None
        fake_item.equipment.equipment_type = "plate"
        mocker.patch("app.services.inventory_service.get_inventory_item", return_value=fake_item)

        fake_character = mocker.Mock()
        fake_character.party_id = 1
        fake_character.current_job.name = "warrior"
        mocker.patch("app.services.inventory_service.get_character_by_id", return_value=fake_character)

        mock_update = mocker.patch("app.services.inventory_service.update_char_equip_repo")
        mock_remove = mocker.patch("app.services.inventory_service.remove_from_inventory")

        equip_from_inventory(user_id=1, inventory_id=7, character_id=3, slot="head")

        mock_update.assert_called_once_with(3, "head", 7)
        mock_remove.assert_not_called()
