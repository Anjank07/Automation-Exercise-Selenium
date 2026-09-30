from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import config

Locator = tuple[str, str]


def slugify(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (saucedemo's data-test naming)."""
    return product_name.lower().replace(" ", "-")


class BasePage:
    """Every interaction goes through an explicit wait. No implicit waits anywhere."""

    def __init__(self, driver: WebDriver, timeout: int = config.DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visit(self, path: str = "/") -> None:
        self.driver.get(config.BASE_URL + path)

    def find(self, locator: Locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: Locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: Locator, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator: Locator, timeout: int = 2) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @staticmethod
    def parse_price(text: str) -> float:
        """'$29.99' or 'Item total: $39.98' -> 29.99 / 39.98"""
        return float(text.split("$")[-1])
