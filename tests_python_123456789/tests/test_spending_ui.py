from time import sleep

import os

import requests
from selene import browser, be, have

from tests_python_123456789.pages.spending_page import spending_page

CATEGORY = 'Food'
AMOUNT = 150.50

class TestSpending:

    def test_spending_title_exists(self, authenticated_user):
        spending_page.check_spending_page_titles()
        sleep(5)

    def test_api_spending_creation(self, api_create_spending):
        # Создаем тестовую трату
        spending = api_create_spending(
            category="Food",
            amount=150.50,
            description="Dinner at restaurant"
        )

        # Проверяем, что трата создана
        assert spending["id"] is not None
        assert spending["amount"] == 150.50

        # 3. Получаем ID созданной траты
        spending_id = spending["id"]

        # 4. Проверяем, что трата существует через GET запрос
        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        get_response = requests.get(
            f"{API_URL}/spends/{spending_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        assert get_response.status_code == 200, "Трата должна существовать после создания"

    def test_create_spending(self, api_create_spending, authenticated_user):
        # spending_page.check_spending_exists(CATEGORY, AMOUNT)
        browser.element('[id^="enhanced-table-checkbox-"]').should(
            have.text('Food')
        )
        sleep(5)

    def test_delete_spending(self, api_delete_spending, authenticated_user):
        spending_page.check_spending_exists(CATEGORY, AMOUNT)
        sleep(5)



