import allure
from selene import browser, have


class RegistrationPage:
    def __init__(self):
        with allure.step("Инициализировать элементы страницы регистрации"):
            self.username = browser.element('input[name=username]')
            self.password = browser.element('input[name=password]')
            self.submit_password = browser.element('input[name=passwordSubmit]')
            self.sing_up_button = browser.element('button[class=form__submit]')
            self.registration_message = browser.element('.form__paragraph')
            self.error_message = browser.element('.form__error')

    def check_registration_message(self):
        with allure.step("Убедиться, что отображается сообщение о регистрации"):
            self.registration_message.with_(timeout=10).should(have.text("Congratulations! You've registered"))
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="successful_registration_message",
                attachment_type=allure.attachment_type.PNG
            )

    def check_already_exist_user(self, username: str):
        with allure.step(f"Убедиться, что отображается ошибка для пользователя {username}"):
            self.error_message.with_(timeout=10).should(have.text(f'Username `{username}` already exists'))
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="existing_user_error",
                attachment_type=allure.attachment_type.PNG
            )

    def check_error_message(self, ):
        with allure.step("Убедиться, что отображается ошибка несовпадения паролей"):
            self.error_message.with_(timeout=10).should(have.text('Passwords should be equal'))
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="password_mismatch_error",
                attachment_type=allure.attachment_type.PNG
            )


registration_page = RegistrationPage()
