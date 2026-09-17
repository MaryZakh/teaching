from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    REGISTRATION_NAV_LINK = (By.CSS_SELECTOR, "[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    REGISTRATION_BTN = (By.XPATH, "//button[text()='Registration']")
    SIGN_OUT_BTN = (By.XPATH,"//*[text()='Sign Out']")

    # def __init__(self, driver):
    #     self.driver = driver


    def open_registration_form(self):
        # self.driver.find_element(*self.REGISTRATION_NAV_LINK).click()
        self.click(self.REGISTRATION_NAV_LINK)

    def fill_email(self,email):
        # self.driver.find_element(*self.EMAIL_INPUT).clear()
        # self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.fill(self.EMAIL_INPUT,email)

    def fill_password(self, password):
        # self.driver.find_element(*self.PASSWORD_INPUT).clear()
        # self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.fill(self.PASSWORD_INPUT,password)

    def submit_registration(self):
        # self.driver.find_element(*self.REGISTRATION_BTN).click()
        self.click(self.REGISTRATION_BTN)

    def is_registered(self):
        try:
            self.wait_until_visible(self.SIGN_OUT_BTN)
            return True
        except TimeoutException:
            return False

    # def get_alert_text(self):
    #     alert = WebDriverWait(self.driver,timeout=5).until(
    #         EC.alert_is_present()
    #     )
    #
    #     return alert.text
    #
    # def accept_alert(self):
    #     self.driver.switch_to.alert.accept()