"""Central test configuration. Env vars override defaults so CI or another
environment can change targets without touching code."""
import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

# Public demo credentials published on the saucedemo login page.
STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
