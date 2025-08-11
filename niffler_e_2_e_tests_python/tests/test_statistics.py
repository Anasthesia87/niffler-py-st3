import allure
import pytest
from typing import List, Dict
from datetime import datetime

@allure.epic("Управление статистикой")
@allure.feature("API тесты статистики расходов")
class TestStatisticsAPI: