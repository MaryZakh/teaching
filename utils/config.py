from os import getenv

from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv("BASE_URL")
TEST_USER_EMAIL = getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = getenv("TEST_USER_PASSWORD")
