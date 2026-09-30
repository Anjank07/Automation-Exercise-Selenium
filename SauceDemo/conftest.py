import os
import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils import config

SCREENSHOT_DIR = Path("reports/screenshots")


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=("chrome", "firefox"))
    parser.addoption("--headless", action="store_true", default=False)


def _chrome(headless: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    if os.getenv("CI"):  # GitHub Actions sets CI=true
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    # Chrome's password manager flags 'secret_sauce' as a breached password and
    # throws a modal over the page after login. Turn that whole feature off.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    return webdriver.Chrome(options=options)  # Selenium Manager resolves the driver


def _firefox(headless: bool) -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)
    return driver


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach each phase's report (rep_setup / rep_call / rep_teardown) to the
    test item so fixtures can see in teardown whether the test failed."""
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drv = _chrome(headless) if browser == "chrome" else _firefox(headless)
    yield drv
    try:
        report = getattr(request.node, "rep_call", None)
        if report is not None and report.failed:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = re.sub(r"[^\w.-]", "_", request.node.name)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            drv.save_screenshot(str(SCREENSHOT_DIR / f"{safe_name}_{stamp}.png"))
    finally:
        drv.quit()  # always runs, even if the screenshot itself fails


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver).open()


@pytest.fixture
def logged_in(login_page) -> InventoryPage:
    return login_page.login(config.STANDARD_USER, config.PASSWORD)
