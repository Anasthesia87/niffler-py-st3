import allure


@allure.epic("Управление пользователями")
@allure.feature("API тесты работы с пользователями")
class TestUsersAPI:

    @allure.story("Получение списка пользователей")
    @allure.title("Успешное получение списка пользователей с пагинацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_users_success(self, users_client):
        with allure.step("Отправить запрос с параметрами по умолчанию"):
            data = users_client.get_all_users(
                page=0,
                size=10,
                sort="username,ASC"
            )

        with allure.step("Проверить структуру ответа"):
            assert isinstance(data, dict), "Ответ должен быть объектом"

            required_keys = {
                "content", "pageable", "totalElements",
                "totalPages", "last", "size", "number"
            }
            missing_keys = required_keys - set(data.keys())
            assert not missing_keys, f"Отсутствуют ключи: {missing_keys}"

    @allure.story("Валидация данных")
    @allure.title("Проверка структуры данных пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_data_structure(self, users_client):
        data = users_client.get_all_users()

        with allure.step("Проверить структуру каждого пользователя"):
            required_fields = {"id", "username", "currency"}
            for user in data["content"]:
                missing_fields = required_fields - set(user.keys())
                assert not missing_fields, \
                    f"У пользователя {user.get('username')} отсутствуют поля: {missing_fields}"

    @allure.story("Пагинация")
    @allure.title("Проверка работы пагинации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination(self, users_client):
        page1 = users_client.get_all_users(page=0, size=10)
        assert len(page1["content"]) == 10, "Должно вернуться 10 пользователей"

        page2 = users_client.get_all_users(page=1, size=10)
        assert len(page2["content"]) == 10, "Должно вернуться 10 пользователей"

        page1_usernames = {u["username"] for u in page1["content"]}
        page2_usernames = {u["username"] for u in page2["content"]}
        assert not page1_usernames & page2_usernames, "Страницы должны содержать разных пользователей"

    @allure.story("Сортировка")
    @allure.title("Проверка сортировки по username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_username(self, users_client):
        users = users_client.get_all_users(sort="username,ASC")["content"]

        usernames = [u["username"] for u in users]
        expected_sorted = sorted(usernames, key=lambda x: x.lower())

        assert usernames == expected_sorted, (
            f"Пользователи должны быть отсортированы по username (case-insensitive)\n"
            f"Ожидаемый порядок: {expected_sorted}\n"
            f"Фактический порядок: {usernames}"
        )
