import logging
from urllib.parse import urljoin
import allure
import requests
import uuid
from typing import Dict, Any
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response


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
        self.session.hooks["response"].append(self.attach_response)

    @staticmethod
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

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

    @allure.step("Получить информацию о расходе")
    def get_spending(self, spending_id: str) -> Any:
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

    @allure.step("Удалить запись о расходе")
    def delete_spending(self, spending_id: str) -> bool:
        url = urljoin(self.base_url, f"/api/spends/remove?ids={spending_id}")
        response = self.session.delete(url)
        response.raise_for_status()
        return True

    @allure.step("Обновить информацию о расходе")
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
