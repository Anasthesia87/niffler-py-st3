import allure
from typing import List, Dict
from ..core.base_session import BaseSession


class NifflerCurrencyClient:
    def __init__(self, session: BaseSession, auth_token: str):
        self.session = session
        self.session.headers.update({
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        })

    @allure.step("Получить все валюты")
    def get_all_currencies(self) -> List[Dict]:
        response = self.session.get("currencies/all")
        response.raise_for_status()
        return response.json()

















