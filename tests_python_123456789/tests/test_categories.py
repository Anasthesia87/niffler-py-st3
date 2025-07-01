from time import sleep

from tests_python_123456789.pages.profile_page import profile_page


class TestCategories:

    def test_add_category(self, add_category):
        profile_page.successful_adding()
        sleep(5)


    def test_add_dublicate_category(self, add_dublicate_category):
        profile_page.check_category_error_message()
        sleep(5)





