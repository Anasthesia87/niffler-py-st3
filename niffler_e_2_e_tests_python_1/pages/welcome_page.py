import allure

from selene import have, be


class WelcomePage:
    def __init__(self, browser):
        self.browser = browser
        self.login_button = browser.element('[class="main__link"][href="/redirect"]')
        self.register_button = browser.element(
            '[class="main__link"][href*="/register"]'
        )
        self.greetings_text = browser.element('[class="main__header"]')
        self.greetings_logo = browser.element('[class="main__logo"]')

    def open(self, url):
        with allure.step("Открываем главную страницу"):
            self.browser.open(f"/")
            self.greetings_logo.wait_until(be.visible)

    def go_to_registration_page(self):
        with allure.step("Переходим на форму регистрации"):
            self.register_button.click()

    def go_to_logging_page(self):
        with allure.step("Переходим на форму входа в приложение"):
            self.login_button.click()

    def check_greeting_text(self, text):
        with allure.step(f"Проверяем успешность наличие приветственного текста"):
            self.browser.element('[src="/images/niffler-logo.png"]').wait_until(
                be.visible
            )
            self.browser.element(self.greetings_text).should(
                have.values_containing(text)
            )