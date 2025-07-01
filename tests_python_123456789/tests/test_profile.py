from time import sleep

from faker import Faker

from tests_python_123456789.pages.profile_page import profile_page


class TestProfile:

    def test_successful_filling_form(self, profile_page_update_name, envs):
        fake = Faker()
        profile_page.check_filling_form(fake.name())


