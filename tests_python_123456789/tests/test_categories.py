from time import sleep

from selene import browser, be

from tests_python_123456789.pages.profile_page import profile_page


class TestCategories:

    def test_add_category(self, add_category):
        profile_page.successful_adding()
        sleep(5)

    def test_empty_name_category(self, authenticated_user):
        browser.element('[aria-label="Menu"]').should(be.clickable).click()
        browser.element('li.MuiMenuItem-root a.nav-link[href="/profile"]').should(be.clickable).click()
        profile_page.check_error_message_adding_empty_name_category()










