import os
from time import sleep

from allure_commons.types import Severity
from selene import have, be
from faker import Faker
from pages.login_page import LoginPage
from pages.main_page import MainPage
import allure

from niffler_e_2_e_tests_python.pages.welcome_page import WelcomePage
from niffler_e_2_e_tests_python.utils.browser_helpers import check_redirect

fake = Faker()


def test_login_valid_creds(login_page, valid_user):
    main_page = login_page.login_with_valid_credentials(**valid_user)







