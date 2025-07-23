from urllib.parse import urljoin
import requests
from typing import Dict, List, Any


class NifflerCategoriesClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': auth_token,  # Уже содержит 'Bearer '
            'Content-Type': 'application/json'
        })

    def get_categories(self) -> List[Dict]:
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return response.json()

    def add_category(
            self,
            name: str,
            username: str = "aslavret",
            archived: bool = False,
            category_id: str = None
    ) -> Dict[str, Any]:
        """Создает новую категорию"""
        if not category_id:
            import uuid
            category_id = str(uuid.uuid4())

        data = {
            "id": category_id,
            "name": name,
            "username": username,
            "archived": archived
        }

        url = urljoin(self.base_url, "/api/categories/add")
        response = self.session.post(url, json=data)

        response.raise_for_status()
        return response.json()

    def update_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновляет существующую категорию
        """
        if 'id' not in category_data:
            raise ValueError("Category data must contain 'id' field")

        url = urljoin(self.base_url, "/api/categories/update")
        response = self.session.patch(url, json=category_data)

        response.raise_for_status()
        return response.json()
