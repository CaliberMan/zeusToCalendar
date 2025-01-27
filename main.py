import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def authenticate(page):
    username = os.getenv("ZEUS_USERNAME")
    password = os.getenv("ZEUS_PASSWORD")

    # "Sign in with Office 365" button
    page.click(".btn.btn-lg.btn-office.mt-2")

    # Wait for the login page to load
    page.wait_for_selector("#i0116")
    page.fill("#i0116", username)
    page.press("#i0116", "Enter")

    # password page
    page.wait_for_selector("#i0118")
    page.fill("#i0118", password)
    page.press("#i0118", "Enter")

def setup_browser():
    browser_path = "/snap/bin/brave"
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir="./brave-user-data",
        executable_path=browser_path,
        headless=False
    )
    return browser, playwright

def navigate_and_download(page):
    page.goto("https://zeus.ionis-it.com/home")

    if "Pour vous connecter, c'est ici :" in page.text_content("body"):
        authenticate(page)

    # Wait for navigation after login
    page.wait_for_load_state("networkidle")

    # Generate an ICS button
    page.click("button.btn.btn-primary-custom.mt-3")

    # Choose the "Group" option
    page.select_option("#type", "group")

    # Choose the group name
    page.fill("#filter", "GITM")
    page.press("#filter", "Enter")

    # click on the group
    page.click("tree-node-content span.ng-star-inserted:text('GITM')")

    # download the ICS file
    with page.expect_download() as download_info:
        page.click("button.btn.btn-primary-custom.ng-star-inserted")
        download = download_info.value
        download_path = os.path.join(os.path.expanduser("~"), "Downloads", download.suggested_filename)
        download.save_as(download_path)

def main():
    browser, playwright = setup_browser()
    page = browser.new_page()
    navigate_and_download(page)
    browser.close()
    playwright.stop()

if __name__ == "__main__":
    main()