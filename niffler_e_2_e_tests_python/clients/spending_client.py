import logging
from urllib.parse import urljoin
import requests
import uuid
from typing import Dict, Any


class NifflerSpendingClient:
    def __init__(self, base_url: str, auth_token: str):
        """
        Клиент для работы с расходами через API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        })

    def create_spending(
            self,
            category: str,
            amount: float,
            description: str = "Test spending",
            currency: str = "USD",
            spend_date: str = "2023-01-01",
            username: str = "aslavret"
    ) -> Dict[str, Any]:
        """
        Создает новую запись о расходе
        """
        url = urljoin(self.base_url, "api/spends/add")

        data = {
            "id": str(uuid.uuid4()),
            "spendDate": spend_date,
            "category": {
                "id": str(uuid.uuid4()),
                "name": category,
                "username": username,
                "archived": False
            },
            "currency": currency,
            "amount": amount,
            "description": description,
            "username": username
        }

        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_spending(self, spending_id: str) -> Any:
        """
        Получает информацию о расходе по ID
        """
        url = urljoin(self.base_url, f"/api/spends/{spending_id}")

        try:
            response = self.session.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting spending {spending_id}: {str(e)}")
            raise

    def delete_spending(self, spending_id: str) -> bool:
        """
        Удаляет запись о расходе
        """
        url = urljoin(self.base_url, f"/api/spends/remove?ids={spending_id}")
        response = self.session.delete(url)
        response.raise_for_status()
        return True

    def update_spending(
            self,
            spending_id: str,
            category: dict,
            amount: float,
            description: str,
            currency: str,
            spend_date: str,
            username: str = "aslavret"
    ) -> Dict[str, Any]:
        """
        Обновляет информацию о расходе по ID
        """
        url = urljoin(self.base_url, "/api/spends/edit")

        data = {
            "id": spending_id,
            "spendDate": spend_date,
            "category": category,
            "currency": currency,
            "amount": amount,
            "description": description,
            "username": username
        }

        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()
