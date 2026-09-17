import pytest

from data.contact_data import fake


PHONE_ALERT_TEXT = (
    "Phone not valid: Phone number must contain only digits! "
    "And length min 10, max 15!"
)
EMAIL_ALERT_TEXT = "Email not valid: must be a well-formed email address"

INVALID_CONTACT_FIELDS = [
    pytest.param("phone", "abcdefghij", PHONE_ALERT_TEXT, id="phone-letters"),
    pytest.param("phone", "05011", PHONE_ALERT_TEXT, id="phone-too-short"),
    pytest.param(
        "phone", fake.numerify("#" * 20), PHONE_ALERT_TEXT, id="phone-too-long"
    ),
    pytest.param(
        "email", "invalid-email-format", EMAIL_ALERT_TEXT, id="invalid-email-format"
    ),
]

SUCCESS_DESCRIPTIONS = [
    pytest.param(None, id="all-fields"),
    pytest.param("", id="required-fields-only"),
]