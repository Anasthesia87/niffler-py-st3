from selene import be
from ..pages.profile_page import profile_page


class TestCategories:

    def test_add_category(self, add_category):
        profile_page.successful_adding()

    def test_empty_name_category(self, authenticated_user):
        profile_page.menu_button.should(be.clickable).click()
        profile_page.profile.should(be.clickable).click()
        profile_page.check_error_message_adding_empty_name_category()
