import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


logger = logging.getLogger(__name__)

class ContactsPage(BasePage):
    CONTACTS_NAV_LINK = (By.CSS_SELECTOR, "[href='/contacts']")
    CONTACT_CARDS = (By.CLASS_NAME, "contact-item_card__2SOIM")
    EDIT_BTN = (By.XPATH, "//button[text()='Edit']")
    EDIT_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Name']")
    EDIT_LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    EDIT_PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Phone']")
    EDIT_EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='email']")
    EDIT_ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='Address']")
    EDIT_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder='desc']")
    EDIT_SAVE_BTN = (By.XPATH, "//button[text()='Save']")
    REMOVE_BTN = (By.XPATH,"//button[text()='Remove']")
    DETAIL_CARD = (By.XPATH, "//button[text()='Edit']/..")

    def open_contacts_list(self):
        self.click(self.CONTACTS_NAV_LINK)
        self.wait_until_url_matches(r"/contacts$")

    def contact_cards_count(self, phone):
        # Считает, сколько карточек контактов с данным телефоном сейчас
        # отображено на странице.
        # Используется, чтобы проверить отсутствие
        # контакта (0 = не сохранился) или дубликаты (>1 = один и тот же
        # телефон сохранён больше одного раза).
        return len(self.driver.find_elements(By.XPATH, f"//h3[text()='{phone}']"))

    def contact_card_visible(self, phone):
        # Ждёт появления карточки с данным телефоном и проверяет, что она
        # видима на странице — используется сразу после сохранения контакта,
        # чтобы убедиться, что он реально появился в списке.
        locator = (By.XPATH, f"//h3[text()='{phone}']")
        return self.wait_until_visible(locator).is_displayed()



    def open_contact_details(self,phone):
        logger.info(f"Opening contact details for phone:{phone}")

        locator = (By.XPATH, f"//h3[text()='{phone}']/..")
        self.click(locator)


    def open_edit_mode(self):
        logger.info("Opening edit mode")
        self.click(self.EDIT_BTN)

    def set_edit_field(self, locator,value):
        self.fill(locator,value)

    def submit_edit(self, expect_text=None):
        logger.info("Submiting contact edit")
        self.click(self.EDIT_SAVE_BTN)
        # После Save приложение остается на карточке контакта (/contacts/<id>),
        # а не возвращается на список (/contacts).
        self.wait_until_url_matches(r"/contacts/\d+$")
        if expect_text:
            # Карточка контакта обновляется с задержкой относительно смены URL,
            # поэтому дожидаемся отредактированного значения именно в ней.
            self.wait_until_text_in_element(self.DETAIL_CARD, expect_text)



    def contact_name_for_phone(self,phone):
        card = self.driver.find_element(By.XPATH, f"//h3[text()='{phone}']/..")
        return card.find_element(By.TAG_NAME,"h2").text

    def get_edit_contact(self,locator):
        return self.find(locator).get_attribute("value")


    def remove_current_contact(self):
        logger.info("Deleting contact")
        self.click(self.REMOVE_BTN)
        self.wait_until_url_matches(r"/contacts$")

    def open_first_contact(self):
        cards = self.driver.find_elements(*self.CONTACT_CARDS)
        first_card = cards[0]
        first_card.click()


    def total_contacts_count(self):
        return len(self.driver.find_elements(*self.CONTACT_CARDS))


    def remove_all_contacts(self):
        logger.info("Deleting all contacts")
        while self.total_contacts_count()>0:
            self.open_first_contact()
            self.remove_current_contact()

