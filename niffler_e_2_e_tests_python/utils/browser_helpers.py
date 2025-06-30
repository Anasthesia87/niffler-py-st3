import allure

from selene import browser


def check_redirect(awaiting_url):
    with allure.step(f"Проверяем успешность редиректа на {awaiting_url}"):
        assert (
            browser.driver.current_url == awaiting_url
        ), f"Редирект не корректен awaiting_url : {awaiting_url} , current_url : {browser.driver.current_url}"