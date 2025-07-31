from datetime import datetime
import allure
from selene import browser, have
from ..models.spend import Spend, Category, SpendAdd
from ..pages.spending_page import spending_page
import logging
from ..databases.spend_db import SpendDb
import os
from sqlmodel import Session, select

CATEGORY_1 = 'Food'
AMOUNT_1 = '150.50 $'
CREATE_DATE_1 = 'Jan 01, 2023'

CATEGORY_2 = 'Vacation'
AMOUNT_2 = '10000.00 $'
CREATE_DATE_2 = 'Jan 01, 2023'

logging.basicConfig(level=logging.INFO)


@allure.epic("Управление расходами")
@allure.feature("Тесты расходов")
class TestSpending:

    @allure.story("UI тесты")
    @allure.title("Проверка заголовков страницы расходов")
    def test_ui_spending_title_exists(self, authenticated_user):
        with allure.step("Проверить заголовки страницы расходов"):
            spending_page.check_spending_page_titles()

    @allure.story("API тесты")
    @allure.title("Создание новой траты через API")
    def test_api_spending_creation(self, spending_client):
        with allure.step("Подготовить тестовые данные"):
            test_data = SpendAdd(
                amount=150.50,
                description="Dinner at restaurant",
                category="Food",
                spend_date="2023-01-01",
                currency="USD",
                username="aslavret"
            )

        with allure.step("Создать новую трату через API"):
            created_spending = spending_client.create_spending(**test_data.model_dump())

        with allure.step("Проверить ответ API"):
            assert isinstance(created_spending, dict), "Ответ должен быть словарем"
            assert "id" in created_spending, "Ответ должен содержать ID траты"
            assert created_spending["id"] is not None, "ID траты не должен быть None"
            assert created_spending["amount"] == test_data.amount, \
                f"Ожидалась сумма {test_data.amount}, получено {created_spending['amount']}"
            assert created_spending["description"] == test_data.description, "Неверное описание траты"
            assert created_spending["currency"] == test_data.currency, "Неверная валюта"

        with allure.step("Получить созданную трату"):
            retrieved_spending = spending_client.get_spending(created_spending["id"])
            assert retrieved_spending is not None, "Трата должна существовать после создания"
            assert retrieved_spending["id"] == created_spending["id"], "ID траты не совпадает"
            assert retrieved_spending["amount"] == created_spending["amount"], "Сумма не совпадает"

    @allure.story("UI тесты")
    @allure.title("Проверка созданной траты в UI")
    # выполнить после def test_api_spending_creation
    def test_ui_verify_api_created_spending(self, authenticated_user):
        with allure.step("Проверить таблицу расходов"):
            rows = browser.all('.spendings-table tbody tr')
            for row in rows:
                with allure.step(f"Проверить строку: {row}"):
                    row.all('td').first.should(have.text(CATEGORY_1))
                    row.all('td').second.should(have.text(AMOUNT_1))
                    row.all('td').third.should(have.text(CREATE_DATE_1))
                    logging.info(f"Найдена строка с данными: {CATEGORY_1}, {AMOUNT_1}, {CREATE_DATE_1}")

    @allure.story("API тесты")
    @allure.title("Удаление траты через API")
    def test_api_delete_spending(self, spending_client):
        with allure.step("Подготовить тестовые данные"):
            test_data = SpendAdd(
                amount=10000.00,
                description="Luxury vacation package",
                category="Vacation",
                spend_date="2023-01-01",
                currency="USD",
                username="aslavret"
            )

        with allure.step("Создать тестовую трату"):
            created_spending = spending_client.create_spending(**test_data.model_dump())
            assert isinstance(created_spending, dict), "Ответ должен быть словарем"
            assert "id" in created_spending, "Ответ должен содержать ID траты"
            assert created_spending["id"] is not None, "ID траты не должен быть None"
            spending_id = created_spending["id"]

        with allure.step("Проверить создание траты"):
            retrieved_spending = spending_client.get_spending(spending_id)
            assert retrieved_spending is not None, "Трата должна существовать перед удалением"
            assert retrieved_spending["id"] == spending_id, "ID полученной траты не совпадает"

        with allure.step("Удалить трату"):
            delete_result = spending_client.delete_spending(spending_id)
            assert delete_result is True, "Удаление должно завершиться успешно"

        with allure.step("Проверить удаление"):
            deleted_spending = spending_client.get_spending(spending_id)
            assert deleted_spending is None, "После удаления трата не должна находиться"

    @allure.story("UI тесты")
    @allure.title("Проверка удаленной траты в UI")
    # выполнить после test_api_delete_spending
    def test_ui_verify_api_deleted_spending(self, authenticated_user):
        with allure.step("Проверить отсутствие удаленной траты"):
            rows = browser.all('.spendings-table tbody tr')
            for row in rows:
                if (row.all('td').first.text == CATEGORY_2 and
                        row.all('td').second.text == AMOUNT_2 and
                        row.all('td').third.text == CREATE_DATE_2):
                    logging.error(f"Строка с данными {CATEGORY_2}, {AMOUNT_2}, {CREATE_DATE_2} все еще существует.")
                    return

            logging.info(f"Строка с данными {CATEGORY_2}, {AMOUNT_2}, {CREATE_DATE_2} успешно удалена.")

    @allure.story("DB тесты")
    @allure.title("Проверка БД после создания траты")
    def test_db_after_api_spending_creation(self, spending_client, categories_client):
        with allure.step("Подготовить тестовые данные"):
            test_data = SpendAdd(
                amount=150.50,
                description="Dinner at restaurant",
                category="Food",
                spend_date="2023-01-01",
                currency="USD",
                username="aslavret"
            )

        with allure.step("Создать трату через API"):
            created_spending = spending_client.create_spending(**test_data.model_dump())
            spending_id = created_spending["id"]

        with allure.step("Проверить запись в БД"):
            db = SpendDb(os.getenv("SPEND_DB_URL"))
            with Session(db.engine) as session:
                db_spending = session.exec(
                    select(Spend).where(Spend.id == spending_id)
                ).first()

                assert db_spending is not None, "Трата не найдена в базе данных"
                assert float(db_spending.amount) == float(test_data.amount), "Сумма не совпадает"

                assert db_spending.description == test_data.description, "Описание не совпадает"
                assert db_spending.currency == test_data.currency, "Валюта не совпадает"
                assert db_spending.username == test_data.username, "Username не совпадает"

                expected_date = datetime.strptime(test_data.spend_date, "%Y-%m-%d").date()
                assert db_spending.spend_date == expected_date, "Дата не совпадает"

                db_category = session.get(Category, db_spending.category_id)
                assert db_category is not None, "Категория не найдена"
                assert db_category.name == test_data.category, "Название категории не совпадает"

                session.delete(db_spending)
                session.commit()

    @allure.story("DB тесты")
    @allure.title("Проверка БД после удаления траты")
    def test_db_after_api_spending_deletion(self, spending_client, categories_client):
        with allure.step("Подготовить тестовые данные"):
            test_data = SpendAdd(
                amount=10000.00,
                description="Luxury vacation package",
                category="Vacation",
                spend_date="2023-01-01",
                currency="USD",
                username="aslavret"
            )

        with allure.step("Создать трату через API"):
            created_spending = spending_client.create_spending(**test_data.model_dump())
            spending_id = created_spending["id"]

        with allure.step("Проверить запись в БД перед удалением"):
            db = SpendDb(os.getenv("SPEND_DB_URL"))
            with Session(db.engine) as session:
                db_spending = session.exec(
                    select(Spend).where(Spend.id == spending_id)
                ).first()
                assert db_spending is not None, "Трата должна существовать в БД перед удалением"

                assert float(db_spending.amount) == float(test_data.amount), "Сумма не совпадает"
                assert db_spending.description == test_data.description, "Описание не совпадает"
                assert db_spending.currency == test_data.currency, "Валюта не совпадает"
                assert db_spending.username == test_data.username, "Username не совпадает"

                expected_date = datetime.strptime(test_data.spend_date, "%Y-%m-%d").date()
                assert db_spending.spend_date == expected_date, "Дата не совпадает"

                db_category = session.get(Category, db_spending.category_id)
                assert db_category is not None, "Категория не найдена"
                assert db_category.name == test_data.category, "Название категории не совпадает"

        with allure.step("Удалить трату через API"):
            delete_result = spending_client.delete_spending(spending_id)
            assert delete_result is True, "Удаление должно завершиться успешно"

        with allure.step("Проверить отсутствие записи в БД"):
            with Session(db.engine) as session:
                deleted_db_spending = session.exec(
                    select(Spend).where(Spend.id == spending_id)
                ).first()

                assert deleted_db_spending is None, "Трата должна быть удалена из БД"

                db_category = session.get(Category, db_spending.category_id)
                assert db_category is not None, "Категория не должна удаляться при удалении траты"

    @allure.story("API тесты")
    @allure.title("Обновление данных траты")
    def test_api_spending_update(self, spending_client):
        with allure.step("Подготовить исходные данные"):
            original_data = {
                "category": "Food",
                "amount": 100.00,
                "description": "Original meal",
                "currency": "USD",
                "spend_date": "2023-01-01",
                "username": "aslavret"
            }
        with allure.step("Создать тестовую трату"):
            created = spending_client.create_spending(**original_data)
            current_category = created["category"]

        with allure.step("Подготовить данные для обновления"):
            update_data = {
                "category": {
                    "id": current_category["id"],
                    "name": "Premium Food",
                    "username": "aslavret",
                    "archived": False
                },
                "amount": 150.00,
                "description": "Updated gourmet meal",
                "currency": "EUR",
                "spend_date": "2023-01-02T00:00:00.000Z",
                "username": "aslavret"
            }

        with allure.step("Выполнить обновление"):
            updated = spending_client.update_spending(
                spending_id=created["id"],
                **update_data
            )

        with allure.step("Проверить обновленные данные"):
            assert updated["id"] == created["id"]
            assert updated["amount"] == 150.00
            assert updated["description"] == "Updated gourmet meal"
            assert updated["category"]["name"] == "Premium Food"

    @allure.story("DB тесты")
    @allure.title("Проверка БД после обновления траты")
    def test_api_spending_update_with_db_check(self, spending_client):
        with allure.step("Подготовить исходные данные"):
            original_data = {
                "category": "Food",
                "amount": 100.00,
                "description": "Original meal",
                "currency": "USD",
                "spend_date": "2023-01-01",
                "username": "aslavret"
            }

        with allure.step("Создать тестовую трату"):
            created = spending_client.create_spending(**original_data)
            current_category = created["category"]

        with allure.step("Подготовить данные для обновления"):
            update_data = {
                "category": {
                    "id": current_category["id"],
                    "name": "Business Lunch",
                    "username": "aslavret",
                    "archived": False
                },
                "amount": 150.00,
                "description": "Updated gourmet meal",
                "currency": "EUR",
                "spend_date": "2023-01-02T00:00:00.000Z",
                "username": "aslavret"
            }

        with allure.step("Выполнить обновление"):
            updated = spending_client.update_spending(
                spending_id=created["id"],
                **update_data
            )

        with allure.step("Проверить данные в БД"):
            db = SpendDb(os.getenv("SPEND_DB_URL"))
            with Session(db.engine) as session:
                db_spending = session.exec(select(Spend).where(Spend.id == created["id"])).first()
                assert db_spending is not None, "Запись не найдена в БД"
                assert float(db_spending.amount) == 150.00, "Сумма в БД не совпадает"
                assert db_spending.description == "Updated gourmet meal", "Описание в БД не совпадает"
                assert db_spending.currency == "EUR", "Валюта в БД не совпадает"

                expected_date = datetime.fromisoformat("2023-01-02T00:00:00.000Z").date()
                assert db_spending.spend_date == expected_date, "Дата в БД не совпадает"

                db_category = session.get(Category, db_spending.category_id)
                assert db_category is not None, "Категория не найдена в БД"
                assert db_category.name == "Business Lunch", "Название категории в БД не совпадает"
                assert db_category.username == "aslavret", "Username категории в БД не совпадает"
                assert db_category.archived is False, "Статус archived категории не совпадает"

                session.delete(db_spending)
                session.commit()
