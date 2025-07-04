import os
import uuid
from time import sleep

import allure
import pytest
from click import password_option

from dotenv import load_dotenv
from faker import Faker
from fastapi import requests
from selene import browser, be, have

from allure_commons.types import AttachmentType

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
def create_spending(category, amount, description, currency, spend_date):
    GATEWAY_URL = os.getenv("GATEWAY_URL")
    TOKEN = os.getenv("TOKEN")

    url = f"{GATEWAY_URL}/spends/add"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    data = {
        "id": str(uuid.uuid4()),  # Добавляем уникальный идентификатор
        "spendDate": spend_date,
        "category": {
            "id": str(uuid.uuid4()),  # Добавляем уникальный идентификатор категории
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
    return response.json()







