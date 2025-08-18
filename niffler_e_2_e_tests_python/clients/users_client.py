from ..core.base_session import BaseSession
from typing import Dict, Optional
import allure


class NifflerUsersClient:
    def __init__(self, session: BaseSession, auth_token: str):
        self.session = session
        self.session.headers.update({
            'Authorization': auth_token,
            'accept': 'application/json'
        })

    @allure.step("Получить список пользователей с пагинацией")
    def get_all_users(
            self,
            page: int = 0,
            size: int = 10,
            sort: Optional[str] = None,
            search_query: Optional[str] = None
    ) -> Dict:
        """Получить список пользователей с пагинацией и сортировкой"""
        params = {
            "page": page,
            "size": size
        }

        if sort:
            params["sort"] = sort

        if search_query:
            params["searchQuery"] = search_query

        response = self.session.get("v2/users/all", params=params)
        response.raise_for_status()
        return response.json()
