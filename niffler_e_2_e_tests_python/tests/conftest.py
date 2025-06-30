import os
import pytest
from allure_commons._allure import attach
from dotenv import load_dotenv
from selene import browser, support
import allure
import faker

from niffler_e_2_e_tests_python.pages.login_page import LoginPage

fake = faker.Faker()

@pytest.fixture(scope="session", autouse=True)
def envs():
    load_dotenv()


@pytest.fixture(scope="function")
@allure.title("Запуск браузера")
def browser_init():
    browser.config.browser_name = 'chrome'
    browser.config.base_url = os.getenv("FRONTEND_URL")
    browser.config.timeout = 4
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser
    browser.quit()

@pytest.fixture()
def login_page(browser_init):
    page = LoginPage(browser_init)
    page.open(os.getenv("AUTH_URL"))  # Теперь работает
    return page




@pytest.fixture()
def main_page(browser_init):
    yield MainPage(browser_init).open(os.getenv("FRONTEND_URL"))


@pytest.fixture()
def profile_page(browser_init):
    yield ProfilePage(browser_init)

@pytest.fixture
def valid_user():
    return {"username": "aslavret8", "password": "aslavret8"}

