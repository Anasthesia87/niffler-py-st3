import os
import time
import uuid
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv
from faker import Faker
from selene import browser, be
from ..clients.categories_client import NifflerCategoriesClient
from ..clients.spending_client import NifflerSpendingClient
from ..models.config import Envs
from ..pages.login_page import login_page
from ..pages.profile_page import profile_page
import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Получает статус теста и делает скриншот при падении.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance = Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("API_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        test_username=os.getenv("USER_NAME"),
        test_password=os.getenv("PASSWORD"),
        registration_url=os.getenv("REGISTRATION_URL"),
        auth_url=os.getenv("AUTH_URL"),
        api_auth_url=os.getenv("API_AUTH_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL")
    )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


@pytest.fixture()
def generate_test_user():
    fake = Faker()
    name = fake.user_name()
    password = fake.password()
    return name, password


@pytest.fixture()
def register_new_user(envs: Envs, generate_test_user):
    username, password = generate_test_user

    browser.open(envs.registration_url)

    login_page.username.should(be.blank).type(username)
    login_page.password.should(be.blank).type(password)
    login_page.submit_password.should(be.blank).type(password)

    login_page.submit_button.should(be.clickable).click()

    yield username, password


@pytest.fixture()
def register_double_user(envs: Envs, register_new_user):
    username, password = register_new_user

    browser.open(envs.registration_url)

    login_page.username.should(be.blank).type(username)
    login_page.password.should(be.blank).type(password)
    login_page.submit_password.should(be.blank).type(password)

    login_page.submit_button.should(be.clickable).click()

    yield username, password


@pytest.fixture
def setup_mismatch_password_test(envs: Envs, generate_test_user):
    username, password = generate_test_user
    wrong_password = password + "123"

    browser.open(envs.registration_url)

    login_page.username.should(be.blank).type(username)
    login_page.password.should(be.blank).type(password)
    login_page.submit_password.should(be.blank).type(wrong_password)

    login_page.submit_button.should(be.clickable).click()

    yield username, password


@pytest.fixture
def authenticated_user(envs: Envs):
    username, password = envs.test_username, envs.test_password

    browser.open(envs.auth_url)
    login_page.sign_in(username, password)

    yield username, password


@pytest.fixture
def authenticated_user_with_wrong_data(envs: Envs):
    username = envs.test_username
    password = '1234567890'

    browser.open(envs.auth_url)
    login_page.sign_in(username, password)

    yield username, password


@pytest.fixture
def profile_page_update_name(authenticated_user, envs):
    profile_page.menu_button.should(be.clickable).click()
    profile_page.profile.should(be.clickable).click()


@pytest.fixture
def generate_category_name():
    fake = Faker()
    return fake.word()


@pytest.fixture
def create_category_via_ui(authenticated_user, envs, generate_category_name):
    profile_page.menu_button.should(be.clickable).click()
    profile_page.profile.should(be.clickable).click()
    profile_page.check_adding_category(generate_category_name)


@pytest.fixture
def get_token_for_api_tests(envs: Envs, authenticated_user):
    # Диагностика - выводим все куки и localStorage
    time.sleep(3)
    print("\n=== Cookies ===")
    for cookie in browser.driver.get_cookies():
        print(f"{cookie['name']}: {cookie['value'][:50]}...")

    print("\n=== LocalStorage ===")
    items = browser.driver.execute_script(
        "return Object.keys(window.localStorage).map(key => "
        "`${key}: ${window.localStorage.getItem(key)}`);"
    )
    for item in items:
        print(item[:100] + "..." if len(item) > 100 else item)

    # Поиск токена в разных местах
    token = None

    # Пробуем получить из кук
    for cookie in browser.driver.get_cookies():
        if any(name in cookie['name'].lower() for name in ['jwt', 'token', 'auth', 'access']):
            token = cookie['value']
            allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
            break

    # Если не нашли в куках, пробуем localStorage
    if not token:
        token = browser.driver.execute_script(
            "return window.localStorage.getItem('id_token') || "
            "window.localStorage.getItem('authToken') || "
            "window.localStorage.getItem('accessToken');"
        )
        allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)

    if not token:
        # Делаем скриншот для диагностики
        browser.driver.save_screenshot("auth_failed.png")
        pytest.fail("Token not found after authentication. Check auth_failed.png and console output")

    return f"Bearer {token}"


@pytest.fixture
def api_get_all_users(envs: Envs, get_token_for_api_tests: str):
    def _get_all_users_with_token(
            page: int = 0,
            search_query: str = "",
            sort: str = "username,ASC"
    ) -> List[Dict]:
        API_URL = envs.gateway_url

        params = {
            "page": page,
            "searchQuery": search_query,
            "sort": sort
        }

        headers = {
            "Authorization": get_token_for_api_tests,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.get(
            f"{API_URL}/v2/users/all",
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        response_data = response.json()
        if isinstance(response_data, list):
            return response_data
        return response_data.get("content", [])

    return _get_all_users_with_token


@pytest.fixture
def api_create_category(envs):
    """Фикстура для создания категории через API."""

    def _create_category(
            name: str,
            username: str = "aslavret",
            archived: bool = False,
    ) -> Dict[str, Any]:
        """
        Создает новую категорию через API

        :param name: Название категории
        :param username: Имя пользователя (по умолчанию "aslavret")
        :param archived: Архивировать ли категорию (по умолчанию False)
        :return: Ответ API в виде словаря
        """

        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        if not all([API_URL, TOKEN]):
            pytest.fail("API_URL or TOKEN environment variables are not set")

        url = f"{API_URL}/categories/add"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        category_id = str(uuid.uuid4())

        data = {
            "id": category_id,
            "name": name,
            "username": username,
            "archived": archived
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            category_data = response.json()

            return category_data


        except Exception as e:

            pytest.fail(f"Unexpected error when creating category: {str(e)}")

    return _create_category


@pytest.fixture
def api_get_categories(envs):
    """Фикстура для получения списка категорий."""

    def _get_categories():
        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        try:
            response = requests.get(
                f"{API_URL}/categories/all",
                headers={
                    "Authorization": f"Bearer {TOKEN}",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            pytest.fail(f"Failed to get categories: {str(e)}")

    return _get_categories


@pytest.fixture
def api_update_category(envs):
    def _update_category(category_data: dict):
        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        response = requests.patch(
            f"{API_URL}/categories/update",
            json=category_data,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }

        )

        response.raise_for_status()

        # Обработка разных форматов ответа
        response_data = response.json()
        if isinstance(response_data, list):
            return response_data
        return response_data.get("content", [])

    return _update_category


@pytest.fixture
def categories_client(get_token_for_api_tests):
    """Фикстура для клиента категорий с готовым токеном"""
    return NifflerCategoriesClient(
        base_url="http://gateway.niffler.dc:8090/api",
        auth_token=get_token_for_api_tests
    )


@pytest.fixture
def spending_client(get_token_for_api_tests):
    """Фикстура для клиента расходов с готовым токеном"""
    return NifflerSpendingClient(
        base_url="http://gateway.niffler.dc:8090/api",
        auth_token=get_token_for_api_tests  # Уже содержит "Bearer "
    )


@pytest.fixture
def api_get_current_user(envs: Envs, get_token_for_api_tests: str):
    def _get_current_user() -> Dict[str, Any]:
        token = get_token_for_api_tests
        url = f"{envs.gateway_url}/users/current"

        response = requests.get(
            url,
            headers={
                "Authorization": token,
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    return _get_current_user


@pytest.fixture
def api_update_user(envs: Envs, get_token_for_api_tests: str):
    def _update_user(user_data: dict) -> dict:
        auth_token = get_token_for_api_tests
        url = f"{envs.gateway_url}/users/update"

        response = requests.post(
            url,
            json=user_data,
            headers={
                "Authorization": auth_token,
                "Content-Type": "application/json"
            },
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    return _update_user
