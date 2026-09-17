import logging

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


logger = logging.getLogger(__name__)


class SeleniumEventListener(AbstractEventListener):

    def before_find(self, by, value, driver):
        # Техническое событие: бизнес-контекст уже записывает Page Object.
        logger.debug("WebDriver find: by=%s, value=%s", by, value)

    def before_click(self, element, driver):
        logger.debug("WebDriver click")

    def before_change_value_of(self, element, driver):
        # Не записываем введенное значение: в нем может находиться пароль.
        logger.debug("WebDriver change value")

    def on_exception(self, exception, driver):
        logger.error("WebDriver exception: %s", exception)