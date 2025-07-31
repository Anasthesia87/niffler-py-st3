import uuid
import allure
from faker import Faker
from ..pages.profile_page import profile_page


@allure.epic("Профиль пользователя")
@allure.feature("UI и API тесты профиля")
class TestProfile:

    @allure.story("UI тесты")
    @allure.title("Успешное обновление данных профиля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ui_successful_filling_form(self, profile_page_update_name, envs):
        fake = Faker()
        with allure.step("Обновить данные профиля"):
            profile_page.check_filling_form(fake.name())

    @allure.story("UI тесты")
    @allure.title("Успешный выход из профиля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_successful_sign_out(self, authenticated_user):
        username, _ = authenticated_user
        with allure.step(f"Выполнить выход для пользователя {username}"):
            profile_page.check_sign_out()

    @allure.story("UI тесты")
    @allure.title("Отправка приглашения другу")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_add_friend_invitation_send(self, register_new_user, authenticated_user):
        username, _ = authenticated_user
        with allure.step(f"Отправить приглашение от пользователя {username}"):
            profile_page.check_add_friends_invitation_send()

    @allure.story("API тесты")
    @allure.title("Получение данных текущего пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_get_current_user(self, api_get_current_user):
        with allure.step("Получить данные текущего пользователя"):
            user_data = api_get_current_user()

        with allure.step("Проверить структуру ответа"):
            assert isinstance(user_data["id"], str)
            assert isinstance(user_data["username"], str)
            assert isinstance(user_data["fullname"], str)
            assert isinstance(user_data["currency"], str)

    @allure.story("API тесты")
    @allure.title("Обновление полного имени пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_update_user_fullname(self, authenticated_user, api_update_user):
        username, _ = authenticated_user
        with allure.step("Сгенерировать новое уникальное имя"):
            new_fullname = "Updated Name " + str(uuid.uuid4())[:8]

        with allure.step("Отправить запрос на обновление"):
            updated_user = api_update_user({
                "username": username,
                "fullname": new_fullname
            })
        with allure.step("Проверить корректность обновления"):
            assert updated_user["username"] == username, "Обновлены данные не того пользователя"
            assert updated_user["fullname"] == new_fullname, "Полное имя не обновилось"

    @allure.story("API тесты")
    @allure.title("Получение списка всех пользователей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_get_all_users(self, api_get_all_users):
        with allure.step("Получить список пользователей"):
            users_data = api_get_all_users(page=0)

        with allure.step("Проверить структуру ответа"):
            assert isinstance(users_data, list)
            assert len(users_data) > 0

            first_user = users_data[0]
            assert "id" in first_user
            assert "username" in first_user
            assert "currency" in first_user

            users_with_friendship = [user for user in users_data if "friendshipStatus" in user]
            assert len(users_with_friendship) > 0

    @allure.story("API тесты")
    @allure.title("Поиск пользователя по username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_search_user_by_username(self, register_new_user, api_get_all_users):
        username, _ = register_new_user
        with allure.step(f"Выполнить поиск пользователя {username}"):
            search_results = api_get_all_users(search_query=username)

        with allure.step("Проверить результаты поиска"):
            assert isinstance(search_results, list), "Должен вернуться список"
            assert len(search_results) > 0, "Должен быть найден хотя бы один пользователь"
            assert any(username.lower() in user["username"].lower() for user in
                       search_results), "Искомый пользователь должен быть в результатах"
            assert any(
                user["username"] == username for user in search_results), "Должен быть найден точный match по username"
