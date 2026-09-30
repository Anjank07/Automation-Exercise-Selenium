from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> "LoginPage":
        self.visit("/")
        return self

    def is_displayed(self) -> bool:
        return self.is_visible(self.LOGIN_BUTTON)

    def _submit(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> InventoryPage:
        """Happy path: returns the page we land on."""
        self._submit(username, password)
        return InventoryPage(self.driver)

    def login_expecting_error(self, username: str, password: str) -> str:
        """Unhappy path: stays on this page and returns the error text."""
        self._submit(username, password)
        return self.text_of(self.ERROR)
