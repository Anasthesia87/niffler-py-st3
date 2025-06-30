import allure

from selene import have, be

from niffler_e_2_e_tests_python.pages.welcome_page import WelcomePage


class LoginPage(WelcomePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser
        self.username_field = browser.element('[name="username"]')
        self.password_field = browser.element('[name="password"]')
        self.submit_login = browser.element('[class="form__submit"]')
        self.sign_up_link = browser.element('[href="/register"]')
        self.login_logo = browser.element('[src="images/niffler-logo.png"]')

    def open_login_page(self):
        with allure.step("Открываем страницу входа в приложение"):
            self.browser.open(f"/")
            self.greetings_logo.wait_until(be.clickable)
            self.login_button.click()
            self.login_logo.wait_until(be.visible)

    def type_username(self, username):
        with allure.step(f"Заполняем поле Username: {username}"):
            self.username_field.type(username)

    def type_password(self, password):
        with allure.step(f"Заполняем поле Password: {password}"):
            self.password_field.type(password)

    def submit_form(self):
        with allure.step("Подтверждаем заполнение формы"):
            self.submit_login.click()

    def go_to_sign_up_page(self):
        with allure.step("Переходим на форму регистрации"):
            self.sign_up_link.click()

    def check_entrance(self):
        with allure.step(
            "Проверяем отображение картинки на главной странице приложения после входа"
        ):
            self.browser.element('[src="/images/niffler-logo.png""]').wait_until(
                be.visible
            )

    def user_session(self, user_name, user_password):
        with allure.step(
            f"Входим в приложение пользователем: {1} с паролем: {2}"
        ):
            self.open_login_page()
            self.type_username()
            self.type_password()
            self.submit_form()

    # def login_with_valid_credentials(self, username: str, password: str):
    #     # with allure.step("Login with valid credentials"):
    #     #     # self.open_sign_up_form()
    #     #     self.username_field()
    #     #     self.password_field()
    #     #     return self.submit_login()
    #
    #         self.type_username('aslavret8')
    #         self.type_password('aslavret8')
    #         self.submit_form()

    def login_with_valid_credentials(self, username, password):
        self.username_field.type(username)
        self.password_field.type(password)
        self.submit_login.click()



    # def is_error_visible(self):
    #     return self.error_message.wait_until(be.visible)

