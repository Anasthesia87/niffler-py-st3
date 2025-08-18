import allure
from selene import browser, be, have

browser.config.timeout = 10


class LoginPage:
    def __init__(self):
        with allure.step("Инициализировать элементы страницы логина"):
            self.login_header = browser.element('h1.header')
            self.username = browser.element('input[name=username]')
            self.password = browser.element('input[name=password]')
            self.submit_password = browser.element('input[name=passwordSubmit]')
            self.submit_button = browser.element('button[type=submit]')
            self.login_button = browser.element('a:nth-child(1)')
            self.create_new_user_button = browser.element('a:nth-child(2)')
            self.error_message = browser.element("//p[@class='form__error']")

    @allure.step("Авторизоваться с логином '{user}' и паролем '{password}'")
    def sign_in(self, user: str, password: str):
        self.username.with_(timeout=10).should(be.blank).type(user)
        self.password.with_(timeout=10).should(be.blank).type(password)
        with allure.step("Нажать кнопку входа"):
            self.submit_button.click()
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="after_login_click",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.step("Проверить сообщение об ошибке")
    def check_error_message(self):
        with allure.step("Убедиться, что сообщение об ошибке отображается"):
            self.error_message.with_(timeout=10).should(
                have.text('Неверные учетные данные пользователя')
            )
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="error_message_visible",
                attachment_type=allure.attachment_type.PNG
            )


login_page = LoginPage()
