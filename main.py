import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from ics import Calendar

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate with Google Calendar API and return a service object."""
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save credentials for next time
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def upload_to_google_calendar(ics_file_path):
    """Parse the ICS file and upload events to Google Calendar."""
    service = authenticate_google_calendar()

    with open(ics_file_path, 'r') as ics_file:
        content = ics_file.read()
        calendars = Calendar.parse_multiple(content)


    for calendar in calendars:
        for event in calendar.events:
            google_event = {
                'summary': event.name,
                'location': event.location if event.location else '',
                'description': event.description if event.description else '',
                'start': {
                    'dateTime': event.begin.format('YYYY-MM-DDTHH:mm:ss'),
                    'timeZone': 'UTC',  # Adjust time zone as needed
                },
                'end': {
                    'dateTime': event.end.format('YYYY-MM-DDTHH:mm:ss'),
                    'timeZone': 'UTC',  # Adjust time zone as needed
                },
            }
            # Insert event into Google Calendar
            service.events().insert(calendarId='primary', body=google_event).execute()

    print(f"Uploaded events to Google Calendar.")


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

    # Go to next week
    # page.click("button.btn[_ngcontent-wwo-c68][mwlcalendarnextview]")

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

    return download_path


def main():
    browser, playwright = setup_browser()
    page = browser.new_page()
    download_file = navigate_and_download(page)
    browser.close()
    playwright.stop()

    upload_to_google_calendar(download_file)


if __name__ == "__main__":
    main()