import logging
from datetime import datetime
from pathlib import Path
import re

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from data.contact_data import create_contact
from data.user_data import existing_user
from pages.add_new_contact_page import ContactPage
from pages.contacts_page import ContactsPage
from pages.login_page import LoginPage
from utils.config import BASE_URL
from utils.logger_config import configure_logging
from utils.selenium_listener import SeleniumEventListener

configure_logging()
logger = logging.getLogger(__name__)
# Храним скриншоты падений рядом с проектом, чтобы их было легко найти.
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"

@pytest.fixture(scope="function")
def driver():

    logger.info("Starting browser session")

    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(BASE_URL)

    # Тесты работают с оберткой, а исходный driver закрывается в teardown.
    yield EventFiringWebDriver(driver, SeleniumEventListener())

    logger.info("Closing browser session")

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Pytest сам вызывает эту функцию после каждой части теста (setup/call/
    # teardown) и ждет, что мы пропустим ее дальше (yield). Нам здесь нужно
    # только одно: сохранить готовый report прямо на item, под именем
    # rep_setup / rep_call / rep_teardown — чтобы забрать его позже в обычной
    # fixture ниже, той же логикой, что мы уже писали для driver.
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(autouse=True)
def save_screenshot_on_failure(request, driver):
    # autouse=True — фикстура подключается к каждому тесту сама, без
    # упоминания в аргументах теста.
    yield

    # К этому моменту тест уже отработал (или упал), и хук выше уже успел
    # положить report на item.
    setup_report = getattr(request.node, "rep_setup", None)
    call_report = getattr(request.node, "rep_call", None)
    failed = (setup_report and setup_report.failed) or (call_report and call_report.failed)
    if not failed:
        # Для успешного теста screenshot не создаем.
        return

    # Создаем папку screenshots, если ее еще нет.
    SCREENSHOTS_DIR.mkdir(exist_ok=True)

    # Получаем время для уникального имени файла.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Заменяем запрещенные символы в имени теста на "_".
    safe_test_name = re.sub(r'[<>:"/\\|?*]', "_", request.node.name)

    # Создаем имя screenshot: имя теста, время и расширение PNG.
    filename = f"{safe_test_name}_{timestamp}.png"

    # Получаем полный путь к будущему файлу.
    screenshot_path = SCREENSHOTS_DIR / filename

    # Пишем в log имя теста с ошибкой.
    logger.error("Test failed: %s", request.node.nodeid)

    # Сохраняем текущий экран браузера в PNG-файл.
    if driver.save_screenshot(str(screenshot_path)):
        # Если файл сохранен, сообщаем об этом в log.
        logger.info("Screenshot saved: %s", screenshot_path)
        # Прикрепляем этот же файл к Allure report — второй screenshot не делаем.
        allure.attach.file(
            str(screenshot_path),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

@pytest.fixture(scope="function")
def authenticated_driver(driver):
    login_page = LoginPage(driver)
    user = existing_user()

    logger.info(f"Logging in user: {user.username}")

    login_page.open_login_form()
    login_page.fill_email(user.username)
    login_page.fill_password(user.password)
    login_page.submit_login()

    return driver


@pytest.fixture(scope="function")
def ensure_min_contacts(authenticated_driver):
    contacts_page = ContactsPage(authenticated_driver)
    contact_page = ContactPage(authenticated_driver)

    contacts_page.open_contacts_list()

    count = contacts_page.total_contacts_count()
    if count<3:
        logger.warning(f"Contact list has {count} contacts (<3), creating test data")

    while contacts_page.total_contacts_count()<3:
        contact_page.create_contact_steps(create_contact())
        contacts_page.open_contacts_list()

    return authenticated_driver







