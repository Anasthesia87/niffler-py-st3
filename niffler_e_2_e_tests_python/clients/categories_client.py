import uuid
from typing import List, Dict, Any
from urllib.parse import urljoin

import allure
import requests
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response

from ..core.base_session import BaseSession


# class NifflerCategoriesClient:
#     def __init__(self, base_url: str, auth_token: str):
#         """
#         Инициализация клиента для работы с категориями
#
#         Args:
#             base_url: Базовый URL API (например, "http://gateway.niffler.dc:8090")
#             auth_token: Токен авторизации (Bearer token)
#         """
#         self.base_url = base_url.rstrip('/')
#         self.session = requests.Session()
#         self.session.headers.update({
#             'Accept': 'application/json',
#             'Authorization': auth_token,
#             'Content-Type': 'application/json'
#         })
#
#     @staticmethod
#     def attach_response(response: Response, *args, **kwargs):
#         """Прикрепление ответа к Allure отчету"""
#         attachment_name = f"{response.request.method} {response.request.url}"
#         allure.attach(
#             body=dump_response(response),
#             name=attachment_name,
#             attachment_type=AttachmentType.TEXT
#         )
#
#     @allure.step("Получить все категории")
#     def get_categories(self) -> List[Dict]:
#         url = f"{self.base_url}/categories/all"
#         response = self.session.get(url)
#         response.raise_for_status()
#         return response.json()
#
#     @allure.step("Добавить новую категорию")
#     def add_category(
#             self,
#             name: str,
#             username: str = "aslavret",
#             archived: bool = False,
#             category_id: str = None
#     ) -> Dict[str, Any]:
#         if not category_id:
#             import uuid
#             category_id = str(uuid.uuid4())
#
#         data = {
#             "id": category_id,
#             "name": name,
#             "username": username,
#             "archived": archived
#         }
#
#         # Используем self.base_url для формирования полного URL
#         url = f"{self.base_url}/categories/add"
#         response = self.session.post(url, json=data)
#         response.raise_for_status()
#         return response.json()
#
#     @allure.step("Обновить категорию")
#     def update_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
#         if 'id' not in category_data:
#             raise ValueError("Category data must contain 'id' field")
#         url = f"{self.base_url}/categories/update"
#         response = self.session.patch(url, json=category_data)
#         response.raise_for_status()
#         return response.json()

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