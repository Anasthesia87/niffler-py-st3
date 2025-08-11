import allure
from typing import List, Dict


@allure.epic("Управление валютами")
@allure.feature("API тесты работы с валютами")
class TestCurrencyAPI:

    @allure.story("Базовые операции с валютами")
    @allure.title("Успешное получение списка всех валют")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_all_currencies_success(self, currencies_client):
        with allure.step("Отправить GET запрос на /api/currencies/all"):
            response = currencies_client.get_all_currencies()

            allure.attach(
                f"Request URL: {response.request.url}\n"
                f"Status Code: {response.status_code}\n"
                f"Response Body: {response.text}",
                name="request_details",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверить успешность ответа"):
            assert response.status_code == 200, \
                f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверить структуру ответа"):
            currencies = response.json()
            assert isinstance(currencies, list), "Ответ должен быть списком"

            required_fields = {"currency", "currencyRate"}
            for currency in currencies:
                missing_fields = required_fields - set(currency.keys())
                assert not missing_fields, \
                    f"В валюте {currency} отсутствуют поля: {missing_fields}"

    @allure.story("Валидация данных")
    @allure.title("Проверка наличия основных валют")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_validate_base_currencies(self, currencies_client):
        with allure.step("Получить список всех валют"):
            currencies: List[Dict] = currencies_client.get_all_currencies().json()

        with allure.step("Проверить наличие обязательных валют"):
            required_currencies = ["RUB", "USD", "EUR", "KZT"]
            currency_codes = {c["currency"] for c in currencies}

            missing_currencies = set(required_currencies) - currency_codes
            assert not missing_currencies, \
                f"Отсутствуют обязательные валюты: {missing_currencies}"

    @allure.story("Валидация данных")
    @allure.title("Проверка корректности курсов валют")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_currency_rates(self, currencies_client):
        with allure.step("Получить актуальные курсы валют"):
            currencies = currencies_client.get_all_currencies().json()

        with allure.step("Проверить корректность курсов"):
            for currency in currencies:
                with allure.step(f"Проверка валюты {currency['currency']}"):
                    assert isinstance(currency["currencyRate"], (int, float)), \
                        "Курс должен быть числом"
                    assert currency["currencyRate"] > 0, \
                        "Курс должен быть положительным"
