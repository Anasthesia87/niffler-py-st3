import allure


@allure.epic("Управление пользователями")
@allure.feature("API тесты работы с пользователями")
class TestUsersAPI:

    @allure.story("Получение списка пользователей")
    @allure.title("Успешное получение списка пользователей с пагинацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_users_success(self, users_client):
        with allure.step("Отправить запрос с параметрами по умолчанию"):
            response = users_client.get_all_users(
                page=0,
                size=10,
                sort="username,ASC"
            )

            allure.attach(
                f"Request URL: {response.request.url}\n"
                f"Status Code: {response.status_code}",
                name="request_details",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 200, \
                f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Проверить структуру ответа"):
            data = response.json()
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
        with allure.step("Получить список пользователей"):
            response = users_client.get_all_users()
            data = response.json()

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
        with allure.step("Запросить первую страницу (10 пользователей)"):
            page1 = users_client.get_all_users(page=0, size=10).json()
            assert len(page1["content"]) == 10, "Должно вернуться 10 пользователей"

        with allure.step("Запросить вторую страницу"):
            page2 = users_client.get_all_users(page=1, size=10).json()
            assert len(page2["content"]) == 10, "Должно вернуться 10 пользователей"

        with allure.step("Проверить, что списки не пересекаются"):
            page1_usernames = {u["username"] for u in page1["content"]}
            page2_usernames = {u["username"] for u in page2["content"]}
            assert not page1_usernames & page2_usernames, "Страницы должны содержать разных пользователей"

    @allure.story("Сортировка")
    @allure.title("Проверка сортировки по username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_username(self, users_client):
        with allure.step("Запросить с сортировкой по username (ASC)"):
            response = users_client.get_all_users(sort="username,ASC")
            users = response.json()["content"]

            allure.attach(
                "\n".join([u["username"] for u in users]),
                name="actual_sort_order",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверить порядок сортировки"):
            usernames = [u["username"] for u in users]

            expected_sorted = sorted(usernames, key=lambda x: x.lower())

            assert usernames == expected_sorted, (
                f"Пользователи должны быть отсортированы по username (case-insensitive)\n"
                f"Ожидаемый порядок: {expected_sorted}\n"
                f"Фактический порядок: {usernames}\n"
                f"Разница: {set(usernames) - set(expected_sorted)}"
            )
