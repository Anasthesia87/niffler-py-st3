from selene import browser, have, be


class ProfilePage:

    def __init__(self):
        self.input_category = browser.element('#category')
        self.menu_button = browser.element('[aria-label="Menu"]')
        self.profile = browser.element('li.MuiMenuItem-root a.nav-link[href="/profile"]')
        self.button_add_category = browser.element('.add-category__input-container button')
        self.successful_alert = browser.element('div.MuiTypography-body1')
        self.unsuccessful_alert = browser.element('.input__helper-text')
        self.error_alert = browser.element('.add-category__input-container button')
        self.error_message = browser.element('div.MuiAlert-message div.MuiTypography-body1')
        self.username = browser.element('#username')
        self.name = browser.element('#name')
        self.button_submit = browser.element('[type="submit"]')
        self.person_icon = browser.element('[data-testid="PersonIcon"]')
        self.profile = browser.element('//li[.="Profile"]')
        self.category_name = lambda name_category: browser.element(f'//span[.="{name_category}"]').should(
            have.text(f"{name_category}"))
        self.name_category = browser.element('input[name=category]')
        self.category_name = lambda name: browser.all('span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
            have.text(name))
        self.category_input = lambda name: browser.element(f'input[value="{name}"]')
        self.parent_element = browser.all('div:has(span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w)')
        self.archive_button = 'button[aria-label="Archive category"]'
        self.confirm_archive = browser.all('button[type=button]').element_by(have.text('Archive'))
        self.archived_button = browser.element('//span[.="Show archived"]')
        self.archived_category = lambda name: browser.all(
            'span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
            have.text(name))

    def successful_adding(self):
        self.successful_alert.should(have.text('You\'ve added new category:'))

    def check_adding_category(self, category):
        self.input_category.type(category).press_enter()

    def check_error_message_adding_empty_name_category(self):
        self.input_category.type('').press_enter()
        self.unsuccessful_alert.should(have.text('Allowed category length is from 2 to 50 symbols'))

    def check_filling_form(self, name):
        self.name.set_value(name)
        self.button_submit.click()
        self.successful_alert.should(have.text('Profile successfully updated'))


profile_page = ProfilePage()
