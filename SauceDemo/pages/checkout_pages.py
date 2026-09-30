"""The three checkout steps live in one module: they're small and only ever
used in sequence."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE = (By.CSS_SELECTOR, "[data-test='continue']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_details(self, first: str, last: str, postal: str) -> "CheckoutInfoPage":
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        return self

    def continue_to_overview(self) -> "CheckoutOverviewPage":
        self.click(self.CONTINUE)
        return CheckoutOverviewPage(self.driver)

    def continue_expecting_error(self) -> str:
        self.click(self.CONTINUE)
        return self.text_of(self.ERROR)


class CheckoutOverviewPage(BasePage):
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH = (By.CSS_SELECTOR, "[data-test='finish']")

    def item_prices(self) -> list[float]:
        return [self.parse_price(el.text) for el in self.find_all(self.ITEM_PRICES)]

    def subtotal(self) -> float:
        return self.parse_price(self.text_of(self.SUBTOTAL))

    def tax(self) -> float:
        return self.parse_price(self.text_of(self.TAX))

    def total(self) -> float:
        return self.parse_price(self.text_of(self.TOTAL))

    def finish(self) -> "CheckoutCompletePage":
        self.click(self.FINISH)
        return CheckoutCompletePage(self.driver)


class CheckoutCompletePage(BasePage):
    HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def header_text(self) -> str:
        return self.text_of(self.HEADER)
