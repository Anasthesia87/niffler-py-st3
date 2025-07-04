import os

import requests





def test_api_spending_creation(self, api_create_spending):
    # Создаем тестовую трату
    spending = api_create_spending(
        category="Food",
        amount=150.50,
        description="Dinner at restaurant"
    )

    # Проверяем, что трата создана
    assert spending["id"] is not None
    assert spending["amount"] == 150.50

    # 3. Получаем ID созданной траты
    spending_id = spending["id"]

    # 4. Проверяем, что трата существует через GET запрос
    API_URL = os.getenv("API_URL")
    TOKEN = os.getenv("TOKEN")

    get_response = requests.get(
        f"{API_URL}/spends/{spending_id}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert get_response.status_code == 200, "Трата должна существовать после создания"


def test_api_delete_spending(self, api_create_spending, api_delete_spending):
    # Создаем тестовую трату
    spending = api_create_spending(
        category="Food",
        amount=150.50,
        description="Dinner at restaurant"
    )

    # Проверяем, что трата создана
    assert spending["id"] is not None
    assert spending["amount"] == 150.50

    # 3. Получаем ID созданной траты
    spending_id = spending["id"]

    # 4. Проверяем, что трата существует через GET запрос
    API_URL = os.getenv("API_URL")
    TOKEN = os.getenv("TOKEN")

    get_response = requests.get(
        f"{API_URL}/spends/{spending_id}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert get_response.status_code == 200, "Трата должна существовать после создания"

    # 3. Удаляем трату через отдельную фикстуру
    delete_result = api_delete_spending(spending_id)
    assert delete_result is True

    # 4. Проверяем, что трата действительно удалена
    API_URL = os.getenv("API_URL")
    TOKEN = os.getenv("TOKEN")

    check_response = requests.get(
        f"{API_URL}/spends/{spending_id}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert check_response.status_code == 404, "Трата должна быть удалена"

