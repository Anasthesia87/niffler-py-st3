import allure
from selene import browser, have, be


class ProfilePage:

    def __init__(self):
        with allure.step("Инициализировать элементы страницы профиля"):
            self.login_header = browser.element('h1.header')
            self.input_category = browser.element('#category')
            self.menu_button = browser.element('[aria-label="Menu"]')
            self.profile = browser.element('li.MuiMenuItem-root a.nav-link[href="/profile"]')
            self.sign_out_button = browser.all('li.MuiMenuItem-root').element_by(
                have.text('Sign out')
            )
            self.title = browser.element('h2.MuiTypography-root.MuiTypography-h6')

            self.confirm_button = browser.element(
                'div.MuiDialog-container button.MuiButton-containedPrimary'
            )
            self.add_friend_button = browser.all('td[class*="MuiTableCell-alignRight"] button').first
            self.successful_invitation_send_alert = browser.element('.MuiAlert-message')

            self.all_people_button = browser.element('[role="menu"] li:nth-child(4) a')
            self.cancel_button = browser.all('button').element_by(have.text('Close'))
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
            self.category_name = lambda name: browser.all(
                'span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
                have.text(name))
            self.category_input = lambda name: browser.element(f'input[value="{name}"]')
            self.parent_element = browser.all('div:has(span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w)')
            self.archive_button = 'button[aria-label="Archive category"]'
            self.confirm_archive = browser.all('button[type=button]').element_by(have.text('Archive'))
            self.archived_button = browser.element('//span[.="Show archived"]')
            self.archived_category = lambda name: browser.all(
                'span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
                have.text(name))

    @allure.step("Проверить добавление категории")
    def successful_adding(self):
        with allure.step("Убедиться, что отображается сообщение об успешном добавлении"):
            self.successful_alert.with_(timeout=10).should(have.text('You\'ve added new category:'))
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="after_category_added",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.step("Добавить категорию '{category}'")
    def check_adding_category(self, category):
        self.input_category.type(category).press_enter()

    @allure.step("Проверить ошибку при добавлении пустой категории")
    def check_error_message_adding_empty_name_category(self):
        self.input_category.type('').press_enter()
        self.unsuccessful_alert.with_(timeout=10).should(have.text('Allowed category length is from 2 to 50 symbols'))
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="empty_category_error",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Обновить профиль с именем '{name}'")
    def check_filling_form(self, name):
        with allure.step("Ввести новое имя"):
            self.name.with_(timeout=10).set_value(name)
        with allure.step("Нажать кнопку сохранения"):
            self.button_submit.click()
        with allure.step("Проверить сообщение об успешном обновлении"):
            self.successful_alert.with_(timeout=10).should(have.text('Profile successfully updated'))
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="profile_update_success",
                attachment_type=allure.attachment_type.PNG
            )

    @allure.step("Выполнить выход из профиля")
    def check_sign_out(self):
        with allure.step("Открыть меню"):
            self.menu_button.with_(timeout=10).should(be.visible).click()
        with allure.step("Выбрать опцию выхода"):
            self.sign_out_button.with_(timeout=10).should(be.visible).click()
        with allure.step("Подтвердить выход"):
            self.title.with_(timeout=10).should(have.text('Want to logout?'))
            self.confirm_button.with_(timeout=10).should(be.visible).click()
        with allure.step("Проверить переход на страницу входа"):
            self.login_header.with_(timeout=10).should(have.text('Log in'))
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="after_sign_out",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Отправить приглашение другу")
    def check_add_friends_invitation_send(self):
        with allure.step("Открыть меню"):
            self.menu_button.with_(timeout=10).should(be.visible).click()
        with allure.step("Перейти в раздел 'All People'"):
            self.all_people_button.with_(timeout=10).should(be.visible).click()
        with allure.step("Нажать кнопку добавления друга"):
            self.add_friend_button.with_(timeout=10).should(be.visible).click()
        with allure.step("Проверить уведомление об отправке"):
            self.successful_invitation_send_alert.with_(timeout=10).should(have.text('Invitation sent to'))
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="friend_invitation_sent",
            attachment_type=allure.attachment_type.PNG
        )


profile_page = ProfilePage()
