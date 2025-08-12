import requests
from typing import Optional


class NifflerUsersClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": auth_token,
            "accept": "application/json"
        }

    def get_all_users(
            self,
            page: int = 0,
            size: int = 10,
            sort: Optional[str] = None,
            search_query: Optional[str] = None
    ) -> requests.Response:
        """Получить список пользователей с пагинацией и сортировкой"""
        params = {
            "page": page,
            "size": size
        }

        if sort:
            params["sort"] = sort

        if search_query:
            params["searchQuery"] = search_query

        return requests.get(
            f"{self.base_url}/v2/users/all",
            headers=self.headers,
            params=params
        )