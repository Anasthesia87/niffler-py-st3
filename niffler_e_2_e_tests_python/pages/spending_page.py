import allure
from selene import browser, have


class SpendingPage:
    def __init__(self):
        with allure.step("Инициализировать элементы страницы расходов"):
            self.history = browser.element('#spendings')
            self.statistics = browser.element('//*[@id="stat"]/h2')
            self.new_spending = browser.element("#react-select-3-placeholder")
            self.spending_container = browser.element('.table.spendings-table td')
            self.amount = browser.element('input[name=amount]')
            self.currency = browser.element('input[name=currency]')
            self.category = browser.element('#react-select-3-input')
            self.spend_date = browser.element('.calendar-wrapper  input[type="text"]')
            self.description = browser.element('input[name=description]')
            self.add_button = browser.element('button[type=submit]')
            self.error_message = browser.element('.add-spending__form .form__error')
            self.checkbox_for_all = browser.element('thead input[type="checkbox"]')
            self.button_delete = browser.element('.spendings__bulk-actions .button_type_small')
            self.successful_delete = browser.element('.Toastify__toast-body div:nth-child(2)')

    @allure.step("Проверить заголовки страницы расходов")
    def check_spending_page_titles(self):
        with allure.step("Проверить заголовок 'History of Spendings'"):
            self.history.with_(timeout=10).should(
                have.text('History of Spendings')
            )
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="spending_page_titles",
                attachment_type=allure.attachment_type.PNG
            )


spending_page = SpendingPage()
