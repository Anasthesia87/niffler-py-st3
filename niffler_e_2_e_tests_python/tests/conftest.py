import os
import uuid
from typing import Dict, Any
import requests
import pytest
from dotenv import load_dotenv
from faker import Faker
from requests import HTTPError
from selene import browser, be
from niffler_e_2_e_tests_python.models.config import Envs
from niffler_e_2_e_tests_python.pages.login_page import login_page
from niffler_e_2_e_tests_python.pages.profile_page import profile_page


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("API_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        test_username=os.getenv("USER_NAME"),
        test_password=os.getenv("PASSWORD"),
        registration_url=os.getenv("REGISTRATION_URL"),
        auth_url=os.getenv("AUTH_URL"),
    )


@pytest.fixture()
def generate_test_user():
    fake = Faker()
    name = fake.user_name()
    password = fake.password()
    return name, password


@pytest.fixture()
def register_new_user(envs: Envs, generate_test_user):
    username, password = generate_test_user

    if envs.registration_url:
        browser.open(envs.registration_url)

        login_page.username.should(be.blank).type(username)
        login_page.password.should(be.blank).type(password)
        login_page.submit_password.should(be.blank).type(password)

        login_page.submit_button.should(be.clickable).click()

        yield username, password


@pytest.fixture()
def register_double_user(envs: Envs, register_new_user):
    username, password = register_new_user

    if envs.registration_url:
        browser.open(envs.registration_url)

        login_page.username.should(be.blank).type(username)
        login_page.password.should(be.blank).type(password)
        login_page.submit_password.should(be.blank).type(password)

        login_page.submit_button.should(be.clickable).click()

        yield username, password
    else:
        pytest.skip("Registration URL not configured")


@pytest.fixture
def setup_mismatch_password_test(envs: Envs, generate_test_user):
    username, password = generate_test_user
    wrong_password = password + "123"

    if envs.registration_url:
        browser.open(envs.registration_url)

    login_page.username.should(be.blank).type(username)
    login_page.password.should(be.blank).type(password)
    login_page.submit_password.should(be.blank).type(wrong_password)

    login_page.submit_button.should(be.clickable).click()

    yield username, password


@pytest.fixture
def authenticated_user(envs: Envs):
    username, password = envs.test_username, envs.test_password

    if envs.auth_url:
        browser.open(envs.auth_url)
    else:
        pytest.skip("Auth URL not configured")
    login_page.sign_in(username, password)

    yield username, password


@pytest.fixture
def authenticated_user_with_wrong_data(envs: Envs):
    username = envs.test_username
    password = '1234567890'

    if envs.auth_url:
        browser.open(envs.auth_url)
    else:
        pytest.skip("Auth URL not configured")
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
def add_category(authenticated_user, envs, generate_category_name):
    profile_page.menu_button.should(be.clickable).click()
    profile_page.profile.should(be.clickable).click()
    profile_page.check_adding_category(generate_category_name)


@pytest.fixture
def api_create_spending(envs):

    def _create_spending(
            category: str,
            amount: float,
            description: str = "Test spending",
            currency: str = "USD",
            spend_date: str = "2023-01-01",
            username: str = "aslavret",
    ) -> Dict[str, Any]:

        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        if not all([API_URL, TOKEN]):
            pytest.fail("API_URL or TOKEN environment variables are not set")

        url = f"{API_URL}/spends/add"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
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

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            spending_data = response.json()

            return spending_data

        except HTTPError as e:
            pytest.fail(f"Failed to create spending: {str(e)}")

    return _create_spending


@pytest.fixture
def api_delete_spending(envs):
    def _delete_spending(spending_id: str) -> bool:
        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        if not all([API_URL, TOKEN]):
            pytest.fail("API_URL or TOKEN environment variables not set")

        url = f"{API_URL}/spends/remove?ids={spending_id}"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json"
        }

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return True
        except HTTPError as e:
            pytest.fail(f"Failed to delete spending {spending_id}: {str(e)}")

    return _delete_spending
