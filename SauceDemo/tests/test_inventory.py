import pytest


# "az" is deliberately excluded: it's the default order, so a test for it would
# pass even if sorting were completely broken.
@pytest.mark.parametrize(
    "option, field, descending",
    [("za", "names", True), ("lohi", "prices", False), ("hilo", "prices", True)],
    ids=["name-z-to-a", "price-low-to-high", "price-high-to-low"],
)
def test_sorting(logged_in, option, field, descending):
    logged_in.sort_by(option)
    values = logged_in.item_names() if field == "names" else logged_in.item_prices()
    assert values == sorted(values, reverse=descending)


def test_add_to_cart_updates_badge(logged_in):
    logged_in.add_to_cart("Sauce Labs Backpack").add_to_cart("Sauce Labs Bike Light")
    assert logged_in.header.cart_count() == 2
