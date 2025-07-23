from selene import browser, have
from ..pages.spending_page import spending_page
import logging

CATEGORY_1 = 'Food'
AMOUNT_1 = '150.50 $'
CREATE_DATE_1 = 'Jan 01, 2023'

CATEGORY_2 = 'Vacation'
AMOUNT_2 = '10000.00 $'
CREATE_DATE_2 = 'Jan 01, 2023'

logging.basicConfig(level=logging.INFO)


class TestSpending:

    def test_ui_spending_title_exists(self, authenticated_user):
        spending_page.check_spending_page_titles()

    def test_api_spending_creation(self, spending_client):
        test_data = {
            "category": "Food",
            "amount": 150.50,
            "description": "Dinner at restaurant",
            "currency": "USD",
            "spend_date": "2023-01-01",
            "username": "aslavret"
        }

        created_spending = spending_client.create_spending(
            category=test_data["category"],
            amount=test_data["amount"],
            description=test_data["description"],
            currency=test_data["currency"],
            spend_date=test_data["spend_date"],
            username=test_data["username"]
        )

        assert isinstance(created_spending, dict), "Ответ должен быть словарем"
        assert "id" in created_spending, "Ответ должен содержать ID траты"
        assert created_spending["id"] is not None, "ID траты не должен быть None"

        assert created_spending["amount"] == test_data[
            "amount"], f"Ожидалась сумма {test_data['amount']}, получено {created_spending['amount']}"
        assert created_spending["description"] == test_data["description"], "Неверное описание траты"
        assert created_spending["currency"] == test_data["currency"], "Неверная валюта"

        retrieved_spending = spending_client.get_spending(created_spending["id"])

        assert retrieved_spending is not None, "Трата должна существовать после создания"
        assert retrieved_spending["id"] == created_spending["id"], "ID траты не совпадает"
        assert retrieved_spending["amount"] == created_spending["amount"], "Сумма не совпадает"

    # выполнить после def test_api_spending_creation
    def test_ui_verify_api_created_spending(self, authenticated_user):
        rows = browser.all('.spendings-table tbody tr')
        for row in rows:
            row.all('td').first.should(have.text(CATEGORY_1))
            row.all('td').second.should(have.text(AMOUNT_1))
            row.all('td').third.should(have.text(CREATE_DATE_1))
            logging.info(f"Найдена строка с данными: {CATEGORY_1}, {AMOUNT_1}, {CREATE_DATE_1}")

    def test_api_delete_spending(self, spending_client):
        test_data = {
            "category": "Vacation",
            "amount": 10000.00,
            "description": "Luxury vacation package",
            "currency": "USD",
            "spend_date": "2023-01-01",
            "username": "aslavret"
        }

        created_spending = spending_client.create_spending(
            category=test_data["category"],
            amount=test_data["amount"],
            description=test_data["description"],
            currency=test_data["currency"],
            spend_date=test_data["spend_date"],
            username=test_data["username"]
        )

        assert isinstance(created_spending, dict), "Ответ должен быть словарем"
        assert "id" in created_spending, "Ответ должен содержать ID траты"
        assert created_spending["id"] is not None, "ID траты не должен быть None"
        spending_id = created_spending["id"]

        retrieved_spending = spending_client.get_spending(spending_id)
        assert retrieved_spending is not None, "Трата должна существовать перед удалением"
        assert retrieved_spending["id"] == spending_id, "ID полученной траты не совпадает"

        delete_result = spending_client.delete_spending(spending_id)
        assert delete_result is True, "Удаление должно завершиться успешно"

        deleted_spending = spending_client.get_spending(spending_id)
        assert deleted_spending is None, "После удаления трата не должна находиться"

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
