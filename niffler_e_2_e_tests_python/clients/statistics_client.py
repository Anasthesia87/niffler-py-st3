import allure
from ..core.base_session import BaseSession
from typing import Dict


class NifflerStatisticsClient:
    def __init__(self, session: BaseSession, auth_token: str):
        self.session = session
        self.session.headers.update({
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        })

    @allure.step("Получить общую статистику расходов")
    def get_total_statistics(self) -> Dict:
        response = self.session.get("v2/stat/total")
        response.raise_for_status()
        return response.json()
