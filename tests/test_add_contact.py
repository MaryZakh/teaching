import logging

import pytest
from faker import Faker

from data.contact_data import create_contact
from data.contact_datasets import INVALID_CONTACT_FIELDS, SUCCESS_DESCRIPTIONS
from pages.add_new_contact_page import ContactPage
from pages.contacts_page import ContactsPage

fake = Faker()
logger = logging.getLogger(__name__)
pytestmark = pytest.mark.regression

@pytest.mark.smoke
@pytest.mark.parametrize("description", SUCCESS_DESCRIPTIONS)
def test_add_contact_success(authenticated_driver, description):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact() if description is None else create_contact(
        description=description
    )
    logger.info(
        "Testing contact creation: description=%s, phone=%s",
        description,
        contact.phone,
    )
    contact_page.create_contact_steps(contact)

    assert contacts_page.contact_card_visible(contact.phone)



def test_add_contact_empty_name(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(name = "")
    logger.info("Testing contact creation with empty name: phone=%s", contact.phone)

    contact_page.create_contact_steps(contact)

    assert contact_page.is_add_button_active()

    contacts_page.open_contacts_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0




def test_add_contact_empty_last_name(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(last_name="")
    logger.info(
        "Testing contact creation with empty last name: phone=%s",
        contact.phone,
    )

    contact_page.create_contact_steps(contact)

    assert contact_page.is_add_button_active()

    contacts_page.open_contacts_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0



#@pytest.mark.skip(reason = "BUG-123: Contact with empty mail")
@pytest.mark.xfail (reason = "BUG-123: Contact with empty mail")
def test_add_contact_empty_email(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(email="")
    logger.info("Testing contact creation with empty email: phone=%s", contact.phone)

    contact_page.create_contact_steps(contact)

    assert contact_page.is_add_button_active()

    contacts_page.open_contacts_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0


def test_add_contact_empty_address(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(address="")
    logger.info(
        "Testing contact creation with empty address: phone=%s",
        contact.phone,
    )

    contact_page.create_contact_steps(contact)

    assert contact_page.is_add_button_active()

    contacts_page.open_contacts_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0


@pytest.mark.parametrize("field, value, expected_alert", INVALID_CONTACT_FIELDS)
def test_add_contact_invalid_field_rejected(
    authenticated_driver, field, value, expected_alert
):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    contact = create_contact(**{field: value})
    logger.info(
        "Testing invalid contact field: field=%s, phone=%s",
        field,
        contact.phone,
    )

    contact_page.create_contact_steps(contact)

    assert contact_page.get_alert_text().strip() == expected_alert
    contact_page.accept_alert()

    assert contact_page.is_add_button_active()

    contacts_page.open_contacts_list()
    assert contacts_page.contact_cards_count(contact.phone) == 0


@pytest.mark.xfail (reason = "BUG-124: Duplicate phone")
def test_add_contact_duplicate_phone_rejected(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    shared_phone = fake.unique.numerify("050##########")
    first_contact = create_contact(phone=shared_phone)
    second_contact = create_contact(phone=shared_phone)
    logger.info("Testing duplicate contact phone: phone=%s", shared_phone)

    contact_page.create_contact_steps(first_contact)
    assert contacts_page.contact_card_visible(shared_phone)

    contact_page.create_contact_steps(second_contact)


    contacts_page.open_contacts_list()
    assert contacts_page.contact_cards_count(shared_phone) == 1
