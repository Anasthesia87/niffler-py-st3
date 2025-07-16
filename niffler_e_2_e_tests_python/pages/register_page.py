from selene import browser, have


class RegistrationPage:
    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.submit_password = browser.element('input[name=passwordSubmit]')
        self.sing_up_button = browser.element('button[class=form__submit]')
        self.registration_message = browser.element('.form__paragraph')
        self.error_message = browser.element('.form__error')

    def check_registration_message(self):
        self.registration_message.with_(timeout=10).should(have.text("Congratulations! You've registered"))

    def check_already_exist_user(self, username: str):
        self.error_message.with_(timeout=10).should(have.text(f'Username `{username}` already exists'))

    def check_error_message(self, ):
        self.error_message.with_(timeout=10).should(have.text('Passwords should be equal'))


registration_page = RegistrationPage()
