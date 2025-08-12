import allure
import pytest
from datetime import datetime


@allure.epic("Управление статистикой")
@allure.feature("API тесты статистики расходов")
class TestStatisticsAPI:

    @allure.story("Получение статистики")
    @allure.title("Успешное получение общей статистики")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_total_statistics_success(self, statistics_client):
        with allure.step("Отправить GET запрос на /api/v2/stat/total"):
            response = statistics_client.get_total_statistics()

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
            stats = response.json()
            allure.attach(
                str(stats),
                name="statistics_response",
                attachment_type=allure.attachment_type.JSON
            )

            assert isinstance(stats, dict), "Ответ должен быть объектом"
            required_fields = {"total", "currency", "statByCategories"}
            missing_fields = required_fields - set(stats.keys())
            assert not missing_fields, \
                f"В ответе отсутствуют поля: {missing_fields}"

    @allure.story("Валидация данных")
    @allure.title("Проверка формата данных статистики")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_statistics_format(self, statistics_client):
        with allure.step("Получить статистику"):
            stats = statistics_client.get_total_statistics().json()

        with allure.step("Проверить основные поля"):
            assert isinstance(stats["total"], (int, float)), "total должен быть числом"
            assert isinstance(stats["currency"], str), "currency должен быть строкой"
            assert len(stats["currency"]) == 3, "currency должен быть 3-символьным кодом"

        with allure.step("Проверить статистику по категориям"):
            stat_by_categories = stats["statByCategories"]
            assert isinstance(stat_by_categories, list), "statByCategories должен быть списком"

            for category in stat_by_categories:
                assert isinstance(category["categoryName"], str), "categoryName должен быть строкой"
                assert isinstance(category["sum"], (int, float)), "sum должен быть числом"
                assert isinstance(category["currency"], str), "currency должен быть строкой"

                # Проверка формата дат
                for date_field in ["firstSpendDate", "lastSpendDate"]:
                    try:
                        datetime.fromisoformat(category[date_field].replace("Z", "+00:00"))
                    except ValueError:
                        pytest.fail(f"Некорректный формат даты в поле {date_field}")

    @allure.story("Валидация данных")
    @allure.title("Проверка логики статистики")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate_statistics_logic(self, statistics_client):
        with allure.step("Получить статистику"):
            stats = statistics_client.get_total_statistics().json()

        with allure.step("Проверить соответствие total и суммы по категориям"):
            total_from_categories = sum(
                category["sum"] for category in stats["statByCategories"]
            )
            assert abs(stats["total"] - total_from_categories) < 0.01, \
                "Общая сумма не соответствует сумме по категориям"
