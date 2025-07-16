from ..pages.login_page import login_page
from ..pages.spending_page import spending_page


class TestLogin:

    def test_ui_successful_login(self, authenticated_user):
        username, _ = authenticated_user
        spending_page.check_spending_page_titles()

    def test_ui_failed_login(self, authenticated_user_with_wrong_data):
        username, _ = authenticated_user_with_wrong_data
        login_page.check_error_message()
