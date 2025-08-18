import logging
import allure
import requests
from typing import Dict, Any, Optional
from niffler_e_2_e_tests_python.core.base_session import BaseSession


class NifflerSpendingClient:
    def __init__(self, session: BaseSession, auth_token: str):
        self.session = session
        self.session.headers.update({
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        })

    @allure.step("Создать новую запись о расходе")
    def create_spending(
            self,
            category: str,
            amount: float,
            description: str = "Test spending",
            currency: str = "USD",
            spend_date: str = "2023-01-01",
            username: str = "aslavret"
    ) -> Dict[str, Any]:
        data = {
            "spendDate": spend_date,
            "category": {
                "name": category,
                "username": username,
                "archived": False
            },
            "currency": currency,
            "amount": amount,
            "description": description,
            "username": username
        }
        return self.session.post("spends/add", json=data).json()

    @allure.step("Получить информацию о расходе")
    def get_spending(self, spending_id: str) -> Optional[Dict]:
        try:
            response = self.session.get(f"spends/{spending_id}")
            if response.status_code == 404:
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting spending {spending_id}: {str(e)}")
            raise

    @allure.step("Удалить запись о расходе")
    def delete_spending(self, spending_id: str) -> None:
        self.session.delete(f"spends/remove?ids={spending_id}")

    @allure.step("Обновить информацию о расходе")
    def update_spending(
            self,
            spending_id: str,
            category: Dict[str, Any],
            amount: float,
            description: str,
            currency: str,
            spend_date: str,
            username: str = "aslavret"
    ) -> Dict[str, Any]:
        data = {
            "id": spending_id,
            "spendDate": spend_date,
            "category": category,
            "currency": currency,
            "amount": amount,
            "description": description,
            "username": username
        }
        return self.session.patch("spends/edit", json=data).json()
