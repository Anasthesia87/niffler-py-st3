

from tests_python_123456789.pages.spending_page import spending_page



class TestSpending:

    def test_spending_title_exists(self, authenticated_user):
        spending_page.check_spending_page_titles()







