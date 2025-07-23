from selene import be
from ..pages.profile_page import profile_page


class TestCategories:

    def test_ui_add_category(self, create_category_via_ui):
        profile_page.successful_adding()

    def test_ui_empty_name_category(self, authenticated_user):
        profile_page.menu_button.should(be.clickable).click()
        profile_page.profile.should(be.clickable).click()
        profile_page.check_error_message_adding_empty_name_category()

    def test_get_categories_success(self, categories_client):
        categories = categories_client.get_categories()

        assert isinstance(categories, list), "Должен вернуться список"

        if categories:  # если есть данные
            assert "id" in categories[0], "Категория должна содержать id"
            assert "name" in categories[0], "Категория должна содержать name"
            assert "username" in categories[0], "Категория должна содержать username"

    def test_api_add_category(self, categories_client, generate_category_name):
        category_name = generate_category_name

        category = categories_client.add_category(
            name=category_name,
            username="aslavret",
            archived=False
        )

        assert category["id"] is not None, "Должен вернуться ID созданной категории"
        assert category["name"] == category_name, "Название категории должно соответствовать"
        assert category["username"] == "aslavret", "Имя пользователя должно соответствовать"
        assert category["archived"] is False, "Категория не должна быть архивирована"

    def test_api_category_name_update_after_creation(self, categories_client, generate_category_name):
        original_name = f"ORIG_{generate_category_name[:15]}"

        category = categories_client.add_category(
            name=original_name,
            username="aslavret",
            archived=False
        )

        assert category["name"] == original_name, "Исходное название должно соответствовать"
        assert not category["archived"], "Категория не должна быть архивирована изначально"

        new_name = f"UPDATED_{generate_category_name[:10]}"
        update_payload = {
            "id": category["id"],
            "name": new_name,
            "username": "aslavret",
            "archived": False
        }

        updated_category = categories_client.update_category(update_payload)

        assert updated_category["name"] == new_name, "Название должно обновиться"
        assert updated_category["id"] == category["id"], "ID категории не должен изменяться"
        assert not updated_category["archived"], "Статус архивации не должен измениться"

        all_categories = categories_client.get_categories()
        found_category = next(
            (cat for cat in all_categories
             if cat["id"] == category["id"]),
            None
        )

        assert found_category is not None, "Категория должна присутствовать в списке"
        assert found_category["name"] == new_name, "Новое название должно сохраняться"
        assert found_category["username"] == "aslavret", "Имя пользователя должно соответствовать"

    def test_api_get_categories_after_add_category(self, categories_client, generate_category_name):
        category = categories_client.add_category(
            name=generate_category_name,
            username="aslavret",
            archived=False
        )

        categories = categories_client.get_categories()

        assert any(
            c["id"] == category["id"] and
            c["name"] == generate_category_name
            for c in categories
        ), "Созданная категория должна присутствовать в списке"

    def test_api_archiving_after_add_category(self, categories_client, generate_category_name):
        category_name = f"TEST_{generate_category_name}"
        category = categories_client.add_category(
            name=category_name,
            username="aslavret",
            archived=False
        )

        assert not category["archived"], "Категория должна создаваться неархивированной"
        assert category["name"] == category_name, "Название категории должно соответствовать"

        update_data = {
            "id": category["id"],
            "name": category["name"],
            "username": category["username"],
            "archived": True
        }

        updated = categories_client.update_category(update_data)

        assert updated["archived"], "Категория должна быть помечена как архивированная"
        assert updated["id"] == category["id"], "ID категории не должен изменяться"
        assert updated["name"] == category["name"], "Название категории не должно измениться"

        all_categories = categories_client.get_categories()
        found = next(
            (c for c in all_categories
             if c["id"] == category["id"] and
             c["name"] == category_name),
            None
        )

        assert found is not None, "Категория должна присутствовать в списке"
        assert found["archived"], "Статус архивации должен сохраняться в списке"
        assert found["username"] == "aslavret", "Имя пользователя должно соответствовать"
