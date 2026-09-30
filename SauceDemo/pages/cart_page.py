from selenium.webdriver.common.by import By

from components.header import Header
from pages.base_page import BasePage, slugify
from pages.checkout_pages import CheckoutInfoPage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")

    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver)
        self.find(self.CHECKOUT_BUTTON)  # wait until the cart has actually rendered

    def item_names(self) -> list[str]:
        # find_elements, not find_all: an empty cart is a valid state to assert on.
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove(self, product_name: str) -> "CartPage":
        self.click((By.CSS_SELECTOR, f"[data-test='remove-{slugify(product_name)}']"))
        return self

    def checkout(self) -> CheckoutInfoPage:
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutInfoPage(self.driver)
