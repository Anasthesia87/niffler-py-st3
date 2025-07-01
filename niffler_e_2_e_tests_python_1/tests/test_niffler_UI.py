import os
from time import sleep
from selene import browser, support
from allure_commons.types import Severity
from selene import have, be
from faker import Faker
from pages.login_page import LoginPage
from pages.main_page import MainPage
import allure

from niffler_e_2_e_tests_python_1.pages.welcome_page import WelcomePage
# from niffler_e_2_e_tests_python_1.tests_python_123456789.conftest import main_page.py, auth_url, global_user, global_password, base_url
from niffler_e_2_e_tests_python_1.utils.browser_helpers import check_redirect
from niffler_e_2_e_tests_python_1.tests.conftest import auth_url, global_user, global_password, base_url

fake = Faker()


# def test_login_valid_creds(login_page):
#     login_page.login_with_valid_credentials('aslavret8', 'aslavret8')
#     login_page.check_entrance()
#
# def test_login_invalid_creds(login_page):
#     login_page.login_with_invalid_credentials('username', 'password')
#     login_page.check_entrance()
#     check_redirect(f"{os.getenv("AUTH_URL")}/login?error")

import allure
from selene import have, be
from niffler_e_2_e_tests_python_1.tests.conftest import global_user, global_password


@allure.feature("Авторизация")
@allure.story("Успешный вход с валидными учетными данными")
def test_login_valid_creds(login_page):
    """
    Тест проверяет успешный вход с валидными учетными данными
    """
    with allure.step("Открываем страницу логина"):
        login_page.open_login_page()

    with allure.step("Проверяем элементы формы до входа"):
        login_page.username_field.should(be.visible)
        login_page.password_field.should(be.visible)
        login_page.submit_login.should(be.visible)

    with allure.step("Вводим валидные учетные данные"):
        login_page.type_username(global_user)
        login_page.type_password(global_password)
        login_page.submit_form()

    with allure.step("Проверяем успешный вход"):
        login_page.check_entrance()

