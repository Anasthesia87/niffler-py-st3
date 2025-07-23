from selene import browser, be, have

browser.config.timeout = 10


class LoginPage:
    def __init__(self):
        self.login_header = browser.element('h1.header')
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.submit_password = browser.element('input[name=passwordSubmit]')
        self.submit_button = browser.element('button[type=submit]')
        self.login_button = browser.element('a:nth-child(1)')
        self.create_new_user_button = browser.element('a:nth-child(2)')
        self.error_message = browser.element("//p[@class='form__error']")

    def sign_in(self, user: str, password: str):
        self.username.with_(timeout=10).should(be.blank).type(user)
        self.password.with_(timeout=10).should(be.blank).type(password)
        self.submit_button.click()

    def check_error_message(self):
        self.error_message.with_(timeout=10).should(have.text('Неверные учетные данные пользователя'))
        self.error_message.with_(timeout=15).should(have.text('Неверные учетные данные пользователя'))

login_page = LoginPage()
