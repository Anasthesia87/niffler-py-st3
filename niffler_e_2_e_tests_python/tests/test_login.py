import allure
from ..pages.login_page import login_page
from ..pages.spending_page import spending_page


@allure.epic("Авторизация пользователя")
@allure.feature("UI тесты авторизации")
class TestLogin:

    @allure.story("Успешная авторизация")
    @allure.title("Проверка успешного входа в систему")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ui_successful_login(self, authenticated_user):
        username, _ = authenticated_user
        with allure.step(f"Проверить отображение страницы расходов для пользователя {username}"):
            spending_page.check_spending_page_titles()

    @allure.story("Неуспешная авторизация")
    @allure.title("Проверка ошибки при неверных учетных данных")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ui_failed_login(self, authenticated_user_with_wrong_data):
        username, _ = authenticated_user_with_wrong_data
        login_page.check_error_message()
