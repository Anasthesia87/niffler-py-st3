import os
import uuid
from time import sleep
from typing import Dict, Any

import requests


import allure
import pytest
from click import password_option

from dotenv import load_dotenv
from faker import Faker
from selene import browser, be, have

from allure_commons.types import AttachmentType
from sqlalchemy.testing.suite.test_reflection import users

from tests_python_123456789.models.config import Envs
from tests_python_123456789.pages.login_page import login_page
from tests_python_123456789.pages.profile_page import profile_page


# pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]

@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        test_username=os.getenv("USER_NAME"),
        test_password=os.getenv("PASSWORD"),
        registration_url=os.getenv("REGISTRATION_URL"),
        auth_url=os.getenv("AUTH_URL"),
    )



# @pytest.fixture
# def generate_test_user():
#     fake = Faker()
#     name = fake.user_name()
#     password = fake.password()
#     return name, password



@pytest.fixture(scope='session')
def auth(envs: Envs) -> str:
    browser.open(envs.frontend_url)
    browser.element('input[name=username]').set_value(envs.test_username)
    browser.element('input[name=password]').set_value(envs.test_password)
    browser.element('button[type=submit]').click()
    token = browser.driver.execute_script('return window.localStorage.getItem("id_token")')
    allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
    return token


@pytest.fixture()
def main_page(auth: str, envs: Envs):
    browser.open(envs.frontend_url)


# @pytest.fixture()
# def register_new_user(envs: Envs):
#     if envs.registration_url:
#         browser.open(envs.registration_url)
#         browser.element('input[name=username]').set_value(envs.test_username)
#         browser.element('input[name=password]').set_value(envs.test_password)
#         browser.element('input[name=passwordSubmit]').set_value(envs.test_password)
#         browser.element('button[type=submit]').click()
#         sleep(5)


@pytest.fixture()
def generate_test_user():
    """Генерирует случайные имя пользователя и пароль"""
    fake = Faker()
    name = fake.user_name()
    password = fake.password()
    return name, password


@pytest.fixture()
def register_new_user(envs: Envs, generate_test_user):
    """Регистрирует нового пользователя через UI и возвращает его данные"""
    username, password = generate_test_user

    if envs.registration_url:
        # 1. Открываем страницу регистрации
        browser.open(envs.registration_url)

        # 2. Заполняем форму регистрации
        browser.element('input[name=username]').should(be.blank).type(username)
        browser.element('input[name=password]').should(be.blank).type(password)
        browser.element('input[name=passwordSubmit]').should(be.blank).type(password)

        # 3. Отправляем форму
        browser.element('button[type=submit]').should(be.clickable).click()

        # 4. Ожидаем завершения регистрации (лучше заменить sleep на явное ожидание)
        sleep(5)  # Временное решение, лучше использовать:
        # browser.should(have.url_containing('/success'))

        # 5. Возвращаем данные пользователя
        yield username, password


@pytest.fixture()
def register_double_user(envs: Envs, register_new_user):
    """Фикстура для тестирования повторной регистрации существующего пользователя"""
    # 1. Сначала регистрируем нового пользователя
    username, password = register_new_user

    # 2. Пытаемся зарегистрировать того же пользователя снова
    if envs.registration_url:
        browser.open(envs.registration_url)

        # Заполняем форму теми же данными
        browser.element('input[name=username]').should(be.blank).type(username)
        browser.element('input[name=password]').should(be.blank).type(password)
        browser.element('input[name=passwordSubmit]').should(be.blank).type(password)

        # Отправляем форму
        browser.element('button[type=submit]').should(be.clickable).click()

        # Возвращаем данные пользователя и ожидаем ошибку в тесте
        yield username, password
    else:
        pytest.skip("Registration URL not configured")


@pytest.fixture
def setup_mismatch_password_test(envs: Envs, generate_test_user):
    """Фикстура с интеграцией PageObject"""
    username, password = generate_test_user
    wrong_password = password + "123"

    if envs.registration_url:
        browser.open(envs.registration_url)

    browser.element('input[name=username]').should(be.blank).type(username)
    browser.element('input[name=password]').should(be.blank).type(password)
    browser.element('input[name=passwordSubmit]').should(be.blank).type(wrong_password)

    # Отправляем форму
    browser.element('button[type=submit]').should(be.clickable).click()

    # Возвращаем данные пользователя и ожидаем ошибку в тесте
    yield username, password


@pytest.fixture
def authenticated_user(envs: Envs):
    """Фикстура выполняет успешный логин и возвращает credentials"""
    username, password = envs.test_username, envs.test_password

    # Выполняем вход
    if envs.auth_url:
        browser.open(envs.auth_url)
    else:
        pytest.skip("Auth URL not configured")
    login_page.sign_in(username, password)

    yield username, password


@pytest.fixture
def authenticated_user_with_wrong_data(envs: Envs, password: str):
    """Фикстура выполняет успешный логин и возвращает credentials"""
    username, password = envs.test_username, password

    # Выполняем вход
    if envs.auth_url:
        browser.open(envs.auth_url)
    else:
        pytest.skip("Auth URL not configured")
    login_page.sign_in(username, password)

    yield username, password


@pytest.fixture
def profile_page_update_name(authenticated_user, envs):
        browser.element('[aria-label="Menu"]').should(be.clickable).click()
        browser.element('li.MuiMenuItem-root a.nav-link[href="/profile"]').should(be.clickable).click()


@pytest.fixture
def generate_category_name():
    fake = Faker()
    return fake.word()


@pytest.fixture
def add_category(authenticated_user, envs, generate_category_name):
    browser.element('[aria-label="Menu"]').should(be.clickable).click()
    browser.element('li.MuiMenuItem-root a.nav-link[href="/profile"]').should(be.clickable).click()
    profile_page.check_adding_category(generate_category_name)


@pytest.fixture
def api_create_spending(envs) -> Dict[str, Any]:
    """Фикстура для создания траты через API с возможностью кастомизации параметров."""

    def _create_spending(
            category: str,
            amount: float,
            description: str = "Test spending",
            currency: str = "USD",
            spend_date: str = "2023-01-01",
            username: str = "aslavret",
            should_cleanup: bool = True
    ) -> Dict[str, Any]:
        """
        Создает трату через API.

        Args:
            category: Название категории
            amount: Сумма траты
            description: Описание траты (по умолчанию "Test spending")
            currency: Валюта (по умолчанию "USD")
            spend_date: Дата траты в формате YYYY-MM-DD (по умолчанию "2023-01-01")
            username: Имя пользователя (по умолчанию "aslavret")
            should_cleanup: Флаг для удаления после использования (по умолчанию True)

        Returns:
            Словарь с данными созданной траты
        """
        API_URL = os.getenv("API_URL")
        if not API_URL:
            pytest.fail("API_URL environment variable is not set")

        TOKEN = os.getenv("TOKEN")
        if not TOKEN:
            pytest.fail("TOKEN environment variable is not set")

        url = f"{API_URL}/spends/add"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        spending_id = str(uuid.uuid4())
        category_id = str(uuid.uuid4())

        data = {
            "id": spending_id,
            "spendDate": spend_date,
            "category": {
                "id": category_id,
                "name": category,
                "username": username,
                "archived": False
            },
            "currency": currency,
            "amount": amount,
            "description": description,
            "username": username
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Бросит исключение для статусов 4XX/5XX

        spending_data = response.json()

        # Добавляем ID для возможной очистки
        if should_cleanup:
            def cleanup():
                delete_url = f"{API_URL}/spends/{spending_id}"
                requests.delete(delete_url, headers=headers)

            # Для pytest можно использовать request.addfinalizer
            # или просто вернуть данные с функцией очистки
            spending_data["cleanup"] = cleanup

        return spending_data

    return _create_spending


@pytest.fixture
def api_delete_spending():
    """Фикстура для удаления траты через API"""

    def _delete_spending(spending_id: str):
        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        if not API_URL or not TOKEN:
            pytest.fail("API_URL or TOKEN environment variables not set")

        url = f"{API_URL}/spends/remove?ids={spending_id}"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json"
        }

        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Проверяет, что статус 200
        return True  # Если статус 200, считаем удаление успешным

    return _delete_spending









