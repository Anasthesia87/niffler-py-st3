import allure


@allure.epic("Управление валютами")
@allure.feature("API тесты работы с валютами")
class TestCurrencyAPI:

    @allure.story("Базовые операции с валютой")
    @allure.title("Успешное получение списка всех валют")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_all_currencies_success(self, currencies_client):
        with allure.step("Отправить GET запрос на получение всех валют"):
            currencies = currencies_client.get_all_currencies()

        with allure.step("Проверить что ответ является списком"):
            assert isinstance(currencies, list), "Ответ должен быть списком"

        with allure.step("Проверить структуру каждой валюты"):
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
            currencies = currencies_client.get_all_currencies()

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
            currencies = currencies_client.get_all_currencies()

        with allure.step("Проверить корректность курсов"):
            for currency in currencies:
                with allure.step(f"Проверка валюты {currency['currency']}"):
                    assert isinstance(currency["currencyRate"], (int, float)), \
                        "Курс должен быть числом"
                    assert currency["currencyRate"] > 0, \
                        "Курс должен быть положительным"
