
from playwright.sync_api import sync_playwright, TimeoutError

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Navigate to the login page
        page.goto("http://localhost:5173/")

        # Click the "Sign In" button
        page.click('a[href="/auth/login"]')

        # Wait for the login form to be visible
        page.wait_for_selector('input[name="id"]', timeout=60000)

        # Fill in the login form and submit
        page.fill('input[name="id"]', "admin@openwebui.com")
        page.fill('input[name="password"]', "admin")
        page.click('button[type="submit"]')

        # Wait for navigation to the main page
        page.wait_for_url("http://localhost:5173/", timeout=60000)

        # Open the settings modal
        page.click('button[aria-label="Settings"]')

        # Click the "Data Controls" tab
        page.click('button[aria-controls="tab-data-controls"]')

        # Wait for the tab to load
        page.wait_for_timeout(1000)

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    except TimeoutError:
        print("Timeout waiting for element. The dev server may still be starting up.")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
