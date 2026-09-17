import allure
import pytest
from faker import Faker
import logging

from data.contact_data import create_contact
from pages.add_new_contact_page import ContactPage
from pages.contacts_page import ContactsPage

fake = Faker()
logger = logging.getLogger(__name__)
pytestmark = pytest.mark.regression

@allure.feature("Contacts")
@allure.story("Edit contact")
@allure.title("Editing a contact's name updates it in the contacts list")
@allure.description(
    "Creates a contact, opens it, changes the Name field, saves, and checks "
    "that the new name is shown for that contact's card in the list."
)
def test_edit_contact_name_updated(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    new_name = fake.first_name()
    logger.info(
        "Updating contact field: field=name, phone=%s, new_value=%s",
        contact.phone,
        new_name,
    )

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_NAME_INPUT, new_name)
    contacts_page.submit_edit(expect_text=new_name)

    assert contacts_page.contact_name_for_phone(contact.phone) == new_name


def test_edit_contact_last_name_updated(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    new_last_name = fake.last_name()
    logger.info(
        "Updating contact field: field=last_name, phone=%s, new_value=%s",
        contact.phone,
        new_last_name,
    )

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_LAST_NAME_INPUT, new_last_name)
    contacts_page.submit_edit(expect_text=new_last_name)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_LAST_NAME_INPUT) == new_last_name


@pytest.mark.smoke
def test_edit_contact_phone_updated(authenticated_driver):
    logger.info("Test: edit_contact_phone_updated")
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    new_phone = fake.unique.numerify("050#######")

    logger.debug(f"Old phone:{contact.phone}")
    logger.debug(f"New phone{new_phone}")
    logger.info(
        "Updating contact field: field=phone, old_phone=%s, new_phone=%s",
        contact.phone,
        new_phone,
    )

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_PHONE_INPUT, new_phone)
    contacts_page.submit_edit()

    assert contacts_page.contact_card_visible(new_phone)
    assert contacts_page.contact_cards_count(contact.phone) == 0


def test_edit_contact_email_updated(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    new_email = fake.unique.email()
    logger.info(
        "Updating contact field: field=email, phone=%s, new_value=%s",
        contact.phone,
        new_email,
    )

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_EMAIL_INPUT, new_email)
    contacts_page.submit_edit(expect_text=new_email)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_EMAIL_INPUT) == new_email


def test_edit_contact_address_updated(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    new_address = fake.city()
    logger.info(
        "Updating contact field: field=address, phone=%s, new_value=%s",
        contact.phone,
        new_address,
    )

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_ADDRESS_INPUT, new_address)
    contacts_page.submit_edit(expect_text=new_address)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_ADDRESS_INPUT) == new_address


@pytest.mark.skip(reason="BUG-130: Editing description saves literal string '[Object Undefined]'")
def test_edit_contact_description_updated(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    new_description = fake.sentence()
    logger.info(
        "Updating contact field: field=description, phone=%s",
        contact.phone,
    )

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_DESCRIPTION_INPUT, new_description)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_DESCRIPTION_INPUT) == new_description


def test_edit_contact_empty_name_rejected(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    logger.info("Testing empty edited name: phone=%s", contact.phone)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_NAME_INPUT, "")
    contacts_page.submit_edit()

    assert contacts_page.contact_name_for_phone(contact.phone) == contact.name


def test_edit_contact_empty_last_name_rejected(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    logger.info("Testing empty edited last name: phone=%s", contact.phone)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_LAST_NAME_INPUT, "")
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_LAST_NAME_INPUT) == contact.last_name


def test_edit_contact_empty_phone_updated(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    logger.info("Testing empty edited phone: phone=%s", contact.phone)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_PHONE_INPUT, "")
    contacts_page.submit_edit()

    assert contacts_page.contact_cards_count(contact.phone) == 1


def test_edit_contact_empty_email_rejected(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    logger.info("Testing empty edited email: phone=%s", contact.phone)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_EMAIL_INPUT, "")
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_EMAIL_INPUT) == contact.email


def test_edit_contact_empty_address_rejected(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    contact = create_contact()
    contact_page.create_contact_steps(contact)
    logger.info("Testing empty edited address: phone=%s", contact.phone)

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_ADDRESS_INPUT, "")
    contacts_page.submit_edit()

    contacts_page.open_contact_details(contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_ADDRESS_INPUT) == contact.address



@pytest.mark.skip


def test_edit_contact_duplicate_phone_negative(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)
    existing_contact = create_contact()
    other_contact = create_contact()
    logger.info(
        "Testing duplicate edited phone: existing_phone=%s, other_phone=%s",
        existing_contact.phone,
        other_contact.phone,
    )
    contact_page.create_contact_steps(existing_contact)
    contact_page.create_contact_steps(other_contact)

    contacts_page.open_contact_details(other_contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_PHONE_INPUT, existing_contact.phone)
    contacts_page.submit_edit()
    assert contacts_page.contact_cards_count(existing_contact.phone) == 1

@pytest.mark.skip
def test_edit_contact_duplicate_email_negative(authenticated_driver):
    contact_page = ContactPage(authenticated_driver)
    contacts_page = ContactsPage(authenticated_driver)

    existing_contact = create_contact()
    other_contact = create_contact()
    logger.info(
        "Testing duplicate edited email: existing_phone=%s, other_phone=%s",
        existing_contact.phone,
        other_contact.phone,
    )

    contact_page.create_contact_steps(existing_contact)
    contact_page.create_contact_steps(other_contact)

    contacts_page.open_contact_details(other_contact.phone)
    contacts_page.open_edit_mode()
    contacts_page.set_edit_field(contacts_page.EDIT_EMAIL_INPUT, existing_contact.email)
    contacts_page.submit_edit()

    contacts_page.open_contact_details(other_contact.phone)
    contacts_page.open_edit_mode()
    assert contacts_page.get_edit_contact(contacts_page.EDIT_EMAIL_INPUT) == other_contact.email