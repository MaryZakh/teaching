from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


logger = logging.getLogger(__name__)
class BasePage:
    def __init__(self,driver):
        self.driver = driver

    def find(self,locator):
        return self.driver.find_element(*locator)

    def wait_until_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_clickable(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_until_url_matches(self, pattern, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_matches(pattern)
        )

    def wait_until_alert_present(self, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.alert_is_present()
        )

    def wait_until_text_in_element(self, locator, text, timeout=5):
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def click(self,locator):
        logger.debug(f"Click on  {locator}")
        self.wait_until_clickable(locator).click()


    def fill(self,locator,value):
        logger.debug("Fill locator: %s", locator)
        element = self.wait_until_visible(locator)
        element.clear()
        element.send_keys(value)


    def get_alert_text(self):
        return self.wait_until_alert_present().text

    def accept_alert(self):
        self.driver.switch_to.alert.accept()