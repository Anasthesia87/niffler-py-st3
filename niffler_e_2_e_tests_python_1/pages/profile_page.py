import allure

from selene import have, be

from niffler_e_2_e_tests_python_1.pages.login_page import LoginPage


class ProfilePage(LoginPage):
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser
        self.name_field = browser.element('[name="firstname"]')
        self.surname_field = browser.element('[name="surname"]')
        self.category_name_field = browser.element('[name="category"]')
        self.create_category_button = browser.element('[class="button  "]')
        self.category_amount_text = browser.element('[name="category"]')
        self.all_categories = browser.element(
            'class="main-content__section-categories"'
        )
        self.header_avatar = browser.element('[class="header__avatar"]')
        self.categories_list = browser.element('[class="categories__item"]')

    def open_profile(self):
        with allure.step("Открываем страницу профайла пользователя"):
            self.browser.open(f"/profile")
            self.header_avatar.wait_until(be.visible)

    def create_category(self, category_name):
        with allure.step(f"Открываем создаем новую категорию трат : {category_name}"):
            self.category_name_field.type(category_name)
            self.create_category_button.shold(have.value("Create")).click()

    def check_category_creation(self):
        with allure.step("Проверяем создание новой категории трат"):
            self.all_categories.should(
                have._not_.exact_text("No spending categories yet!")
            )
            self.categories_list.should(be.present)