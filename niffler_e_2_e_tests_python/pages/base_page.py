from selene import browser, have

class BasePage:
    def __init__(self):
        self.add_spending_button_link = browser.element('a:has-text("New spending")')
        # Или альтернативный вариант:
        # self.add_spending_button_link = browser.all('a').element_by(have.text("New spending"))