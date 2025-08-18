from selene import browser, have
import allure
from ..pages.register_page import registration_page


@allure.epic("Регистрация пользователя")
@allure.feature("UI тесты регистрации")
class TestRegistration:

    @allure.story("Успешная регистрация")
    @allure.title("Проверка успешной регистрации нового пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ui_successful_registration(self, register_new_user):
        with allure.step("Проверить сообщение об успешной регистрации"):
            registration_page.check_registration_message()

    @allure.story("Ошибки регистрации")
    @allure.title("Проверка ошибки при повторной регистрации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ui_double_registration(self, register_double_user):
        username, _ = register_double_user
        with allure.step(f"Проверить сообщение об ошибке для пользователя {username}"):
            registration_page.check_already_exist_user(username)

    @allure.story("Ошибки регистрации")
    @allure.title("Проверка ошибки при несовпадении паролей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ui_mismatch_password(self, setup_mismatch_password_test):
        username, password = setup_mismatch_password_test
        with allure.step("Проверить сообщение об ошибке несовпадения паролей"):
            registration_page.check_error_message()
        with allure.step("Проверить, что остались на странице регистрации"):
            browser.should(have.url_containing('/register'))
