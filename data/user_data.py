from faker import Faker

from models.user import User
from utils.config import TEST_USER_EMAIL, TEST_USER_PASSWORD

fake = Faker()


def create_user(username=None, password=None):
    return User(
        username=username if username is not None else fake.unique.email(),
        password=password if password is not None else fake.password(
            length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
        )
    )

INVALID_EMAIL = "margogmail.com"
INVALID_PASSWORD = "Mmar123"


def existing_user():
    return create_user(username=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)

def invalid_email_user():
    return create_user(username=INVALID_EMAIL, password=TEST_USER_PASSWORD)

def invalid_password_user():
    return create_user(username=TEST_USER_EMAIL, password=INVALID_PASSWORD)

