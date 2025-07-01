import os
from time import sleep

from selene import browser, have

from tests_python_123456789.pages.spending_page import spending_page
from tests_python_123456789.pages import login_page
from tests_python_123456789.pages import register_page
from tests_python_123456789.pages.register_page import registration_page


class TestRegistration:

    def test_successful_registration(self, register_new_user):
        registration_page.check_registration_message()
        sleep(5)



    def test_double_registration(self, register_double_user):
        """Тест проверяет, что система запрещает повторную регистрацию"""
        username, _ = register_double_user
        registration_page.check_already_exist_user(username)
        sleep(5)



    def test_mismatch_password(self, setup_mismatch_password_test):
        """
            Тест проверяет, что система корректно обрабатывает случай,
            когда пароль и подтверждение пароля не совпадают
            """
        username, password = setup_mismatch_password_test

        # 1. Проверяем сообщение об ошибке

        registration_page.check_error_message()
        sleep(5)

        # 2. Проверяем, что остались на странице регистрации

        browser.should(have.url_containing('/register'))











