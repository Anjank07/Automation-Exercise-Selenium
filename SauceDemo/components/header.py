from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Header(BasePage):
    """Shared header (cart + burger menu) present on every logged-in page.
    Composed into pages rather than inherited, so LoginPage doesn't get it."""

    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def cart_count(self) -> int:
        # find_elements (no wait) on purpose: an empty cart has NO badge,
        # and "0" is a valid answer we shouldn't pay a full timeout for.
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def click_cart(self) -> None:
        self.click(self.CART_LINK)

    def logout(self) -> None:
        self.click(self.MENU_BUTTON)
        # The menu slides in; element_to_be_clickable waits out the animation.
        self.click(self.LOGOUT_LINK)
