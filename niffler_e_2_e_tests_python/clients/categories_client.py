import uuid
from typing import List, Dict, Any
import allure
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response
from ..core.base_session import BaseSession


class NifflerCategoriesClient:
    def __init__(self, session: BaseSession, auth_token: str):
        """
        Инициализация клиента для работы с категориями

        Args:
            session: Готовая сессия BaseSession (уже содержит base_url)
            auth_token: Токен авторизации (Bearer token)
        """
        self.session = session
        self.session.headers.update({
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        })
        self.session.hooks["response"].append(self.attach_response)

    @staticmethod
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    @allure.step("Получить все категории")
    def get_categories(self) -> List[Dict]:
        """Теперь используем относительный путь"""
        response = self.session.get("categories/all")  # Без ведущего слеша
        response.raise_for_status()
        return response.json()

    @allure.step("Добавить новую категорию")
    def add_category(self, name: str, **kwargs) -> Dict[str, Any]:
        data = {
            "id": str(uuid.uuid4()),
            "name": name,
            **kwargs
        }
        response = self.session.post("categories/add", json=data)
        response.raise_for_status()
        return response.json()

    @allure.step("Обновить категорию")
    def update_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'id' not in category_data:
            raise ValueError("Category data must contain 'id' field")
        response = self.session.patch("categories/update", json=category_data)
        response.raise_for_status()
        return response.json()
