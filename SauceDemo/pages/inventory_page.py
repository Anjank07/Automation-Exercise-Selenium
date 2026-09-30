from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from components.header import Header
from pages.base_page import BasePage, slugify
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver)

    @staticmethod
    def _add_button(product_name: str):
        return (By.CSS_SELECTOR, f"[data-test='add-to-cart-{slugify(product_name)}']")

    def title(self) -> str:
        return self.text_of(self.TITLE)

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        self.click(self._add_button(product_name))
        return self

    def item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def item_prices(self) -> list[float]:
        return [self.parse_price(el.text) for el in self.find_all(self.ITEM_PRICES)]

    def sort_by(self, option_value: str) -> "InventoryPage":
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option_value)
        return self

    def open_cart(self) -> CartPage:
        self.header.click_cart()
        return CartPage(self.driver)

    def logout(self):
        from pages.login_page import LoginPage  # local import avoids a circular import
        self.header.logout()
        return LoginPage(self.driver)
