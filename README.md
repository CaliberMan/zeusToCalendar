# Zeus to Google Calendar

This project automates the process of downloading an ICS file from the Zeus website and importing it into your Google Calendar.

## Prerequisites

- Python 3.6 or higher
- Google Cloud Project with Calendar API enabled
- `credentials.json` file from Google Cloud Project

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/CaliberMan/zeusToCalendar.git
    cd zeusToCalendar
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/0) file in the project directory and add your Zeus credentials:

    ```env
    ZEUS_USERNAME=your_username
    ZEUS_PASSWORD=your_password
    ```

5. Place the `credentials.json` file from your Google Cloud Project in the project directory.

## Usage

1. Run the main script to download the ICS file from Zeus:

    ```sh
    python main.py
    ```

2. Run the script to import the downloaded ICS file into your Google Calendar:

    ```sh
    python import_to_google_calendar.py
    ```
