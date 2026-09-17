import logging
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    LOGIN_NAV_LINK = (By.CSS_SELECTOR, "[href='/login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='Login']")
    SIGN_OUT_BTN = (By.XPATH,"//*[text()='Sign Out']")

    # def __init__(self, driver):
    #     self.driver = driver


    def open_login_form(self):
        # self.driver.find_element(*self.LOGIN_NAV_LINK).click()
        logger.info("Opening login form")
        self.click(self.LOGIN_NAV_LINK)


    def fill_email(self,email):
        # self.driver.find_element(*self.EMAIL_INPUT).clear()
        # self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.fill(self.EMAIL_INPUT,email)


    def fill_password(self, password):
        # self.driver.find_element(*self.PASSWORD_INPUT).clear()
        # self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.fill(self.PASSWORD_INPUT, password)

    def submit_login(self):
        self.click(self.LOGIN_BTN)

    # def is_logged(self):
    #     try:
    #         self.driver.find_element(*self.SIGN_OUT_BTN)
    #         return True
    #     except NoSuchElementException:
    #         return False


    def is_logged(self):
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