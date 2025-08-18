import time
import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from allure_commons.types import AttachmentType
from typing import Optional
from niffler_e_2_e_tests_python.models.config import Envs


class TokenManager:
    def __init__(self, envs: Envs, driver: WebDriver):
        with allure.step("Инициализация TokenManager"):
            self.envs = envs
            self.driver = driver

    def _get_token_from_cookies(self) -> Optional[str]:
        with allure.step("Поиск токена в cookies"):
            for cookie in self.driver.get_cookies():
                if any(name in cookie['name'].lower() for name in ['jwt', 'token', 'auth', 'access']):
                    token = cookie['value']
                    with allure.step(f"Найден токен в cookie: {cookie['name']}"):
                        allure.attach(token, name="token_from_cookies.txt", attachment_type=AttachmentType.TEXT)
                        return token
            with allure.step("Токен не найден в cookies"):
                return None

    def _get_token_from_storage(self) -> Optional[str]:
        with allure.step("Поиск токена в хранилище браузера"):
            try:
                if not self.driver.current_url.startswith('data:'):
                    token = self.driver.execute_script(
                        "return window.localStorage.getItem('id_token') || "
                        "window.localStorage.getItem('authToken') || "
                        "window.localStorage.getItem('accessToken') || "
                        "window.sessionStorage.getItem('id_token') || "
                        "window.sessionStorage.getItem('authToken') || "
                        "window.sessionStorage.getItem('accessToken');"
                    )
                    if token:
                        with allure.step("Токен найден в хранилище"):
                            allure.attach(token, name="token_from_storage.txt", attachment_type=AttachmentType.TEXT)
                            return token
                    with allure.step("Токен не найден в хранилище"):
                        return None
            except Exception as e:
                with allure.step(f"Ошибка при доступе к хранилищу: {str(e)}"):
                    return None

    def get_token(self) -> str:
        with allure.step("Получение токена аутентификации"):
            with allure.step("Ожидание завершения аутентификации (3 сек)"):
                time.sleep(3)

            with allure.step("Попытка получить токен из разных источников"):
                token = self._get_token_from_cookies() or self._get_token_from_storage()

            if not token:
                with allure.step("Токен не найден - создание скриншота"):
                    self.driver.save_screenshot("auth_failed.png")
                    pytest.fail("Token not found after authentication. Check auth_failed.png")

            with allure.step("Токен успешно получен"):
                allure.attach(token, name="auth_token.txt", attachment_type=AttachmentType.TEXT)
                return f"Bearer {token}"
