import os

import allure
from selene import browser, be, have



class RegistrationPage:
    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.submit_password = browser.element('input[name=passwordSubmit]')
        self.sing_up_button = browser.element('button[class=form__submit]')
        self.registration_message = browser.element('.form__paragraph')
        self.error_message = browser.element('.form__error')


    @allure.step('UI: registration user')
    def sign_up(self, user: str, password: str, submit_password: str):
        self.username.should(be.blank).type(user)
        self.password.should(be.blank).type(password)
        self.submit_password.should(be.blank).type(submit_password)
        self.sing_up_button.click()


    @allure.step('UI: check title')
    def check_registration_message(self):
        self.registration_message.should(have.text("Congratulations! You've registered"))


    @allure.step('UI: check text about user')
    def check_already_exist_user(self, username: str):
        self.error_message.should(have.text(f'Username `{username}` already exists'))


    @allure.step('UI: check text about error')
    def check_error_message(self, ):
        self.error_message.should(have.text('Passwords should be equal'))


registration_page = RegistrationPage()