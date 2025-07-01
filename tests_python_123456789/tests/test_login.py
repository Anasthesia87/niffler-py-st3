from tests_python_123456789.pages.login_page import login_page
from tests_python_123456789.pages.spending_page import spending_page


class TestLogin:

    def test_successful_login(self, authenticated_user):
        """Тест успешного входа в систему"""
        username, _ = authenticated_user
        spending_page.check_spending_page_titles()

    def test_failed_login(self, authenticated_user_with_wrong_data):
        username, _ = authenticated_user_with_wrong_data
        login_page.check_category_error_message()








