from selene import browser, have
from ..pages.register_page import registration_page


class TestRegistration:

    def test_ui_successful_registration(self, register_new_user):
        registration_page.check_registration_message()

    def test_ui_double_registration(self, register_double_user):
        username, _ = register_double_user
        registration_page.check_already_exist_user(username)

    def test_ui_mismatch_password(self, setup_mismatch_password_test):
        username, password = setup_mismatch_password_test
        registration_page.check_error_message()
        browser.should(have.url_containing('/register'))
