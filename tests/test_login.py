import logging

import allure
import pytest

from data.user_data import existing_user
from data.user_datasets import INVALID_LOGIN_USERS
from pages.login_page import LoginPage


logger = logging.getLogger(__name__)
pytestmark = pytest.mark.regression


@allure.feature("Login")
@allure.story("Successful login")
@allure.title("Existing user can log in with correct email and password")
@allure.description(
    "Opens the login form, fills in a known valid user's credentials, "
    "submits, and checks that the app shows the logged-in state (Sign Out button)."
)
@pytest.mark.smoke
def test_login_success(driver):
    login_page = LoginPage(driver)
    user = existing_user()

    logger.info("Testing successful login: username=%s", user.username)

    login_page.open_login_form()
    login_page.fill_email(user.username)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.is_logged() is True


@pytest.mark.parametrize("user_factory", INVALID_LOGIN_USERS)
def test_login_rejected(driver, user_factory):
    login_page = LoginPage(driver)
    user = user_factory()

    logger.info(
        "Testing rejected login: case=%s, username=%s",
        user_factory.__name__,
        user.username,
    )

    login_page.open_login_form()
    login_page.fill_email(user.username)
    login_page.fill_password(user.password)
    login_page.submit_login()

    assert login_page.get_alert_text() == "Wrong email or password"
    login_page.accept_alert()
