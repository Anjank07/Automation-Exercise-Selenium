import pytest

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


def test_remove_item_empties_cart(logged_in):
    cart = logged_in.add_to_cart("Sauce Labs Backpack").open_cart()
    cart.remove("Sauce Labs Backpack")
    assert cart.item_names() == []
    assert cart.header.cart_count() == 0


def test_checkout_requires_postal_code(logged_in):
    info = logged_in.add_to_cart("Sauce Labs Backpack").open_cart().checkout()
    error = info.fill_details("Anjan", "Kumar", "").continue_expecting_error()
    assert error == "Error: Postal Code is required"


@pytest.mark.smoke
def test_end_to_end_checkout(logged_in):
    for product in PRODUCTS:
        logged_in.add_to_cart(product)

    cart = logged_in.open_cart()
    assert sorted(cart.item_names()) == sorted(PRODUCTS)

    overview = cart.checkout().fill_details("Anjan", "Kumar", "342001").continue_to_overview()

    # Validate the maths, not just that the page loaded.
    assert overview.subtotal() == pytest.approx(sum(overview.item_prices()))
    assert overview.total() == pytest.approx(overview.subtotal() + overview.tax())

    assert overview.finish().header_text() == "Thank you for your order!"
