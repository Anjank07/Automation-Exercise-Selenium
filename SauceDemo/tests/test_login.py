import pytest

from utils import config


@pytest.mark.smoke
def test_valid_login_lands_on_products(login_page):
    inventory = login_page.login(config.STANDARD_USER, config.PASSWORD)
    assert inventory.title() == "Products"


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        (config.LOCKED_OUT_USER, config.PASSWORD,
         "Epic sadface: Sorry, this user has been locked out."),
        (config.STANDARD_USER, "wrong_password",
         "Epic sadface: Username and password do not match any user in this service"),
        ("", config.PASSWORD, "Epic sadface: Username is required"),
        (config.STANDARD_USER, "", "Epic sadface: Password is required"),
    ],
    ids=["locked-out-user", "wrong-password", "empty-username", "empty-password"],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    assert login_page.login_expecting_error(username, password) == expected_error


def test_logout_returns_to_login(logged_in):
    login_page = logged_in.logout()
    assert login_page.is_displayed()
