import os
import requests
from selene import browser, have
from ..pages.spending_page import spending_page

CATEGORY_1 = 'Food'
AMOUNT_1 = '150.50 $'
CREATE_DATE_1 = 'Jan 01, 2023'

CATEGORY_2 = 'Vacation'
AMOUNT_2 = '10000.00 $'
CREATE_DATE_2 = 'Jan 01, 2023'

import logging

logging.basicConfig(level=logging.INFO)


class TestSpending:

    def test_spending_title_exists(self, authenticated_user):
        spending_page.check_spending_page_titles()

    def test_api_spending_creation(self, api_create_spending):
        spending = api_create_spending(
            category="Food",
            amount=150.50,
            description="Dinner at restaurant"
        )

        assert spending["id"] is not None
        assert spending["amount"] == 150.50

        spending_id = spending["id"]

        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        get_response = requests.get(
            f"{API_URL}/spends/{spending_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        assert get_response.status_code == 200, "Трата должна существовать после создания"

    # выполнить после def test_api_spending_creation
    def test_ui_verify_api_created_spending(self, authenticated_user):
        rows = browser.all('.spendings-table tbody tr')
        for row in rows:
            row.all('td').first.should(have.text(CATEGORY_1))
            row.all('td').second.should(have.text(AMOUNT_1))
            row.all('td').third.should(have.text(CREATE_DATE_1))
            logging.info(f"Найдена строка с данными: {CATEGORY_1}, {AMOUNT_1}, {CREATE_DATE_1}")

    def test_api_delete_spending(self, api_create_spending, api_delete_spending):
        spending = api_create_spending(
            category="Vacation",
            amount=10000.00,
            description="Luxury vacation package"
        )

        assert spending["id"] is not None
        assert spending["amount"] == 10000.00

        spending_id = spending["id"]

        API_URL = os.getenv("API_URL")
        TOKEN = os.getenv("TOKEN")

        get_response = requests.get(
            f"{API_URL}/spends/{spending_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        assert get_response.status_code == 200, "Трата должна существовать после создания"

        if api_delete_spending(spending_id):
            logging.info("Трата успешно удалена.")
        else:
            logging.error("Не удалось удалить трату.")

        check_response = requests.get(
            f"{API_URL}/spends/{spending_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        assert check_response.status_code == 404, "Трата должна быть удалена"

    # выполнить после test_api_delete_spending
    def test_ui_verify_api_deleted_spending(self, authenticated_user):
        rows = browser.all('.spendings-table tbody tr')
        for row in rows:
            if (row.all('td').first.text == CATEGORY_2 and
                    row.all('td').second.text == AMOUNT_2 and
                    row.all('td').third.text == CREATE_DATE_2):
                logging.error(f"Строка с данными {CATEGORY_2}, {AMOUNT_2}, {CREATE_DATE_2} все еще существует.")
                return

        logging.info(f"Строка с данными {CATEGORY_2}, {AMOUNT_2}, {CREATE_DATE_2} успешно удалена.")
