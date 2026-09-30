# Design Decisions

Why each choice was made, and what the alternatives were.

## 1. Selenium Manager instead of webdriver-manager
Since Selenium 4.6, `webdriver.Chrome()` downloads and caches the matching driver on its
own. Using `webdriver-manager` would add a third-party dependency to solve a problem
the library already solves.

## 2. Explicit waits only, never implicit
All waiting lives in `BasePage` via `WebDriverWait` + `expected_conditions`.
Selenium's docs warn against mixing implicit and explicit waits because the timeouts
interact unpredictably. An implicit wait also applies to *every* `find_element`, which
makes "element is absent" checks slow. `time.sleep()` is never used: it is either too
long, which wastes time, or too short, which causes flaky tests.

Each wait uses the condition the action actually needs:
- `visibility_of_element_located` before reading or typing, because an element can be
  in the DOM but hidden.
- `element_to_be_clickable` before clicking. This matters for logout, where the side
  menu slides in and the link isn't clickable until the animation finishes.

## 3. Deliberate use of `find_elements` with no wait
`Header.cart_count()` and `CartPage.item_names()` use `find_elements`, which returns an
empty list immediately. For these, *absence is a valid answer*: an empty cart has no
badge. Waiting for the badge would burn the full timeout every time the correct result
is 0. This is the one place where not waiting is correct.

## 4. Locator strategy: `data-test` attributes first
SauceDemo exposes `data-test` attributes, which exist purely for automation. Unlike
CSS classes or text, developers don't change them for styling or copy reasons.
Priority order: `data-test` → `id` → CSS → XPath.
The burger menu and logout link use `id` because those elements are identified most
clearly that way. XPath isn't needed anywhere here, and I'd only use it for things CSS
can't do, such as matching by text or walking up to a parent element.

**Known trade-off:** add and remove buttons are found by turning the product name into
a slug (`Sauce Labs Backpack` → `add-to-cart-sauce-labs-backpack`). This is simple, but
it breaks for names with special characters, such as `Test.allTheThings() T-Shirt (Red)`.
The more robust alternative is a relative XPath that anchors on the product name and
walks up to its card.

## 5. Page Object Model with fluent returns
- Locators are class-level tuples, so tests never touch `By.*`. A UI change means
  editing one file.
- Methods that cause navigation return the next page object
  (`cart.checkout()` → `CheckoutInfoPage`). This makes the test read like the user journey.
- Happy and unhappy paths are separate methods (`login` vs `login_expecting_error`).
  One method returning "maybe a page, maybe an error" would force `if` statements
  into tests.
- Assertions live in tests, not page objects. Pages report state; tests decide whether
  that state is correct.

## 6. Header as a component, composed rather than inherited
The cart badge and menu appear on every logged-in page but not on the login page.
Putting them in `BasePage` would give `LoginPage` methods it can't use. Composition
(`self.header = Header(driver)`) matches the component-object pattern in the Playwright
repo.

## 7. pytest fixtures, not unittest `setUp`
- The `yield` fixture keeps setup and teardown together.
- The fixture chain `driver → login_page → logged_in` lets each test request exactly the
  starting state it needs.
- Driver scope is **function**, so every test gets a fresh browser. SauceDemo stores
  the cart in localStorage, so a shared session would leak cart state between tests
  and make results depend on test order. This costs some speed. That's the right trade
  at 13 tests. At 500 tests I'd consider a session-scoped driver with state reset
  between tests.

## 8. Screenshot on failure via `pytest_runtest_makereport`
The hook attaches each phase's report to the test item. The driver fixture then checks
`rep_call.failed` during teardown. The screenshot is taken inside `try/finally` so
`driver.quit()` always runs, even if the screenshot fails. This prevents orphaned browser
processes in CI.

## 9. Data-driven tests with `@pytest.mark.parametrize`
Four negative login cases come from one test function, and `ids=` gives each a readable
name in reports. Sorting skips the `az` case on purpose: it's the default order, so that
test would pass even if sorting were broken. **A test that can't fail has no value.**

## 10. The end-to-end test checks the maths, not just the page
It asserts that the subtotal equals the sum of the item prices, and the total equals
the subtotal plus tax. Reaching the "Thank you" page only proves navigation works. The
calculation is the business-critical part.

## 11. Chrome's password-leak popup is disabled
Recent Chrome versions flag `secret_sauce` as a breached password and show a modal
after login, which blocks clicks. The password manager preferences are turned off in the
driver options. This is a real-world issue, not a theoretical one.

## 12. CI configuration
- `--no-sandbox` and `--disable-dev-shm-usage` are added only when `CI` is set.
  Containers have a small `/dev/shm`, which crashes Chrome, but these flags aren't
  needed locally.
- `--strict-markers` turns a typo like `@pytest.mark.smok` into an error instead of
  letting it silently fall out of the smoke run.
- Reports are uploaded with `if: always()`. The report matters most when a run fails.

## 13. Pinned dependency versions
`requirements.txt` uses `==` so a run today and a run in six months use the same code.
Upgrades then happen deliberately, not by surprise.
