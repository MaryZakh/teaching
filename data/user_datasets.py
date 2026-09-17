import pytest

from data.user_data import (
    create_user,
    invalid_email_user,
    invalid_password_user,
)


INVALID_LOGIN_USERS = [
    pytest.param(invalid_email_user, id="invalid-email"),
    pytest.param(invalid_password_user, id="invalid-password"),
    pytest.param(create_user, id="unregistered-user"),
]

INVALID_REGISTRATION_USERS = [
    pytest.param(invalid_email_user, id="invalid-email"),
    pytest.param(invalid_password_user, id="invalid-password"),
]