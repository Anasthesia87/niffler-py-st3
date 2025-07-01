# import os
# import pytest
# from allure_commons._allure import attach
# from dotenv import load_dotenv
# from selene import browser, support
# import allure
# import faker
#
# from niffler_e_2_e_tests_python_1.pages.login_page import LoginPage
#
# fake = faker.Faker()
#
# @pytest.fixture(scope="session", autouse=True)
# def envs():
#     load_dotenv()
#
#
# @pytest.fixture(scope="function")
# @allure.title("Запуск браузера")
# def browser_init():
#     browser.config.browser_name = 'chrome'
#     browser.config.base_url = os.getenv("FRONTEND_URL")
#     browser.config.timeout = 4
#     browser.config.window_width = 1920
#     browser.config.window_height = 1080
#
#     yield browser
#     browser.quit()
#
# @pytest.fixture()
# def login_page(browser_init):
#     page = LoginPage(browser_init)
#     page.open(os.getenv("AUTH_URL"))  # Теперь работает
#     return page
#
#
# @pytest.fixture()
# def main_page.py(browser_init):
#     yield MainPage(browser_init).open(os.getenv("FRONTEND_URL"))
#
#
# @pytest.fixture()
# def profile_page(browser_init):
#     yield ProfilePage(browser_init)


import pytest
from selene import browser
from faker import Faker
from dotenv import load_dotenv
import os

from niffler_e_2_e_tests_python_1.pages.login_page import LoginPage

load_dotenv()
fake = Faker()

global_user = os.getenv("TEST_LOGIN")
global_password = os.getenv("TEST_PASSWORD")

auth_url = os.getenv("BASE_AUTH_URL")
base_url = os.getenv("BASE_URL")

@pytest.fixture(scope='function')
def setup_browser():
    browser.config.driver_name = 'chrome'
    browser.config.base_url = base_url
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield browser
    browser.quit()



@pytest.fixture()
def login_page(setup_browser):
    page = LoginPage(setup_browser)
    page.open(os.getenv("AUTH_URL"))  # Теперь работает
    return page

# @pytest.fixture(scope="function")
# def create_user(setup_browser):
#     browser.open(f"{auth_url}register")
#
#     username = fake.user_name()
#     password = fake.password()
#
#     # Первый раз надо раскомментировать и создать пользователя
#     signup_page = SignupPage(browser)
#     signup_page.signup(username, password)
#
#     browser.should(have.url_containing("http://frontend.niffler.dc/main"))
#     browser.should(have.url_containing("http://auth.niffler.dc:9000/login"))
#     browser.should(have.title("Login to Niffler"))
#
#     yield username, password


@pytest.fixture(scope="function")
def signin_user(setup_browser):
    browser.open(f"{auth_url}login")

    browser.element('[placeholder="Type your username"]').type(global_user)
    browser.element('[placeholder="Type your password"]').type(global_password)
    browser.element('button:has-text("Log in")').click()

    browser.should(have.url_containing(f"{base_url}main"))

    yield global_user, global_password