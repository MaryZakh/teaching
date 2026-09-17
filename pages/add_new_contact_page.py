import logging

from selenium.webdriver.common.by import By


from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ContactPage(BasePage):
    ADD_NAV_LINK = (By.CSS_SELECTOR, "[href = '/add']")
    NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Name']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Phone']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='email']")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='Address']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder='description']")
    SAVE_BTN = (By.XPATH, "//button[b[text()='Save']]")
    CONTACT_NAV_LINK = (By.CSS_SELECTOR,"[href='/contacts']")

    # def __init__(self, driver):
    #     self.driver = driver

    def open_contact_form(self):
        # self.driver.find_element(*self.ADD_NAV_LINK).click()
        self.click(self.ADD_NAV_LINK)

    def fill_name(self, name):
        # self.driver.find_element(*self.NAME_INPUT).clear()
        # self.driver.find_element(*self.NAME_INPUT).send_keys(name)
        self.fill(self.NAME_INPUT,name)

    def fill_last_name(self, last_name):
        # self.driver.find_element(*self.LAST_NAME_INPUT).clear()
        # self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.fill(self.LAST_NAME_INPUT, last_name)

    def fill_phone(self, phone):
        # self.driver.find_element(*self.PHONE_INPUT).clear()
        # self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)
        self.fill(self.PHONE_INPUT, phone)

    def fill_email(self, email):
        # self.driver.find_element(*self.EMAIL_INPUT).clear()
        # self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.fill(self.EMAIL_INPUT,email)

    def fill_address(self, address):
        # self.driver.find_element(*self.ADDRESS_INPUT).clear()
        # self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)
        self.fill(self.ADDRESS_INPUT,address)

    def fill_description(self, description):
        # self.driver.find_element(*self.DESCRIPTION_INPUT).clear()
        # self.driver.find_element(*self.DESCRIPTION_INPUT).send_keys(description)
        self.fill(self.DESCRIPTION_INPUT,description)

    def fill_contact_form(self, contact):
        self.fill_name(contact.name)
        self.fill_last_name(contact.last_name)
        self.fill_phone(contact.phone)
        self.fill_email(contact.email)
        self.fill_address(contact.address)
        self.fill_description(contact.description)

    def submit_contact(self):
        # self.driver.find_element(*self.SAVE_BTN).click()
        self.click(self.SAVE_BTN)


    def is_add_button_active(self):
        add_link = self.find(self.ADD_NAV_LINK)
        return "active" in add_link.get_attribute("class")


    def create_contact_steps(self, contact):
        logger.info(f"Creating contact:{contact.phone}")
        self.open_contact_form()
        self.fill_contact_form(contact)
        self.submit_contact()
        self.wait_until_url_matches(r"/contacts$")







