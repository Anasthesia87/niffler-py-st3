import allure

from selene import be, have

from niffler_e_2_e_tests_python.pages.login_page import LoginPage


class MainPage(LoginPage):
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser
        self.category_drop_down_list = self.browser.element(
            '[id="react-select-21-input"]'
        )
        self.spend_amount_field = self.browser.element('[name="amount"]')
        self.spend_description = self.browser.element('name="description"')
        self.spending_submit_button = self.browser.element('[class="button  "]')
        self.spending_table = self.browser.element('[class="table spendings-table"]')
        self.table_records = self.browser.element('[class="value-container"]')
        self.set_all_spending = self.browser.element(
            '//*[@id="root"]/div/div[2]/main/div/section[3]/div/table/thead/tr/th[1]/input'
        )
        self.delete_selected_spending = self.browser.element(
            '//*[@id="root"]/div/div[2]/main/div/section[3]/div/div/div/section[2]/button'
        )

    def check_records_table(self, is_present):
        with allure.step(
                f"Проверяем отсутствие/присутствие таблицы с тратами: {is_present}"
        ):
            if is_present:
                self.spending_table.should(be.present)
            else:
                self.spending_table.should(be.not_.present)

