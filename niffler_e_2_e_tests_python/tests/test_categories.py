import pytest
from selene import be
from niffler_e_2_e_tests_python.pages.profile_page import profile_page


class TestCategories:


    def test_add_category_via_ui(self, create_category_via_ui):
        profile_page.successful_adding()

    def test_empty_name_category(self, authenticated_user):
        profile_page.menu_button.should(be.clickable).click()
        profile_page.profile.should(be.clickable).click()
        profile_page.check_error_message_adding_empty_name_category()

    def test_add_category_via_api(self, api_create_category, generate_category_name):
        """Тест создания категории через API."""

        # Создаем новую категорию
        category = api_create_category(
            name=generate_category_name,
            username="aslavret",
            archived=False
        )

        # Проверяем ответ
        assert category["id"] is not None, "Должен вернуться ID созданной категории"
        assert category["name"] == generate_category_name, "Название категории должно соответствовать"
        assert category["username"] == "aslavret", "Имя пользователя должно соответствовать"
        assert category["archived"] is False, "Категория не должна быть архивирована"



    def test_get_categories_after_add_category_via_api(self, api_create_category, generate_category_name, api_get_categories):
        """Тест с использованием фикстуры для получения категорий."""

        # Создаем новую категорию
        category = api_create_category(
            name=generate_category_name,
            username="aslavret",
            archived=False
        )

        # Получаем список категорий
        categories = api_get_categories()

        # Проверяем наличие созданной категории
        assert any(
            category["id"] == category["id"] and
            category["name"] == generate_category_name
            for category in categories
        ), "Созданная категория должна присутствовать в списке"





    def test_archiving_after_add_category_via_api(
            self,
            api_create_category,
            api_update_category,
            api_get_categories,
            generate_category_name
    ):
        """Тест архивации категории с использованием фикстур."""
        # 1. Создаем категорию со случайным именем
        category_name = f"TEST_{generate_category_name}"
        category = api_create_category(
            name=category_name,
            username="aslavret",
            archived=False
        )

        # Проверяем начальное состояние
        assert category["archived"] is False, "Категория должна создаваться неархивированной"
        assert category["name"] == category_name, "Название категории должно соответствовать"

        # 2. Архивируем категорию
        update_data = {
            "id": category["id"],
            "name": category["name"],  # Можно изменить, если нужно
            "username": category["username"],
            "archived": True  # Основное изменение
        }

        updated = api_update_category(update_data)

        # 3. Проверяем непосредственный результат обновления
        assert updated["archived"] is True, "Категория должна быть помечена как архивированная"
        assert updated["id"] == category["id"], "ID категории не должен изменяться"
        assert updated["name"] == category["name"], "Название категории не должно измениться"

        # 4. Проверяем через список категорий
        all_categories = api_get_categories()
        found = next(
            (c for c in all_categories
             if c["id"] == category["id"] and
             c["name"] == category_name),
            None
        )

        assert found is not None, "Категория должна присутствовать в списке"
        assert found["archived"] is True, "Статус архивации должен сохраняться в списке"
        assert found["username"] == "aslavret", "Имя пользователя должно соответствовать"





    def test_category_name_update_after_creation_via_api(
            self,
            api_create_category,
            api_update_category,
            api_get_categories,
            generate_category_name
    ):
        """
        Проверка изменения названия категории после её создания.
        Шаги:
        1. Создать новую категорию
        2. Обновить название через API
        3. Проверить обновленные данные
        4. Убедиться, что изменения сохраняются при получении
        """
        # 1. Создаем тестовую категорию
        original_name = f"ORIG_{generate_category_name[:15]}"
        category = api_create_category(
            name=original_name,
            username="aslavret",
            archived=False
        )

        # Проверяем начальные условия
        assert category["name"] == original_name, "Исходное название должно соответствовать"

        # 2. Подготавливаем данные для обновления
        new_name = f"UPDATED_{generate_category_name[:10]}"
        update_payload = {
            "id": category["id"],
            "name": new_name,  # Новое название
            "username": "aslavret",
            "archived": False  # Статус архивации не меняем
        }

        # 3. Выполняем обновление
        updated_category = api_update_category(update_payload)

        # Проверяем непосредственный результат
        assert updated_category["name"] == new_name, "Название должно обновиться"
        assert updated_category["id"] == category["id"], "ID категории не должен изменяться"
        assert not updated_category["archived"], "Статус архивации не должен измениться"

        # 4. Проверяем через отдельный запрос
        all_categories = api_get_categories()
        found_category = next(
            (cat for cat in all_categories
             if cat["id"] == category["id"]),
            None
        )

        assert found_category is not None, "Категория должна присутствовать в списке"
        assert found_category["name"] == new_name, "Новое название должно сохраняться"
        assert found_category["username"] == "aslavret", "Имя пользователя должно соответствовать"













