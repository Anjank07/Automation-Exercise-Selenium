# Selenium + pytest UI Automation — SauceDemo

A small, deliberately lean UI test framework for [saucedemo.com](https://www.saucedemo.com),
built with Selenium 4, pytest and the Page Object Model. It's a companion to my larger
[Playwright project](https://github.com/Anjank07/automation-exercise-playwright).

## Stack
Python 3.12 · Selenium 4 (Selenium Manager) · pytest · pytest-html · GitHub Actions

## Structure
```
pages/          Page objects: login, inventory, cart, checkout (3 steps)
components/     Header component (cart badge, burger menu) shared by logged-in pages
utils/config.py Base URL, timeouts, test users (env-overridable)
tests/          13 tests: login, sorting, cart, checkout
conftest.py     Driver fixture, --browser / --headless options, screenshot on failure
```

## Coverage
| Area | Tests |
|---|---|
| Login | valid login, 4 data-driven negative cases, logout |
| Inventory | sorting (3 orders), add to cart updates badge |
| Cart & checkout | remove item, required-field validation, end-to-end order with price-total verification |

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                      # full suite, Chrome, headed
pytest --headless           # headless
pytest --browser firefox    # Firefox
pytest -m smoke             # critical path only
```
The HTML report is written to `reports/report.html`. Failure screenshots go to `reports/screenshots/`.

## CI
Every push and PR runs the full suite headless on GitHub Actions. The report and any
screenshots are uploaded as a build artifact, even when tests fail.

Design reasoning: see [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).
