# Automation Testing Project

This project is an automation testing framework for web applications using Python, Selenium, and pytest. It focuses on testing the functionality of the Amazon website using the Page Object Model (POM) design pattern.

## Features

- **Selenium** for browser automation.
- **pytest-html** for generating detailed HTML reports.
- **Logging** to capture test execution details.
- **Screenshots** taken on test failures for better debugging.

## Prerequisites

- **Python 3.12** or later.
- **Microsoft Edge WebDriver** matching your browser version.
- A **virtual environment** (recommended).

## Project Structure

automation_test_project/ │ ├─── tests/ │ ├── conftest.py # Contains fixture setup for WebDriver and hooks │ ├── test_login.py # Contains the test cases │ ├─── Pages/ │ └── page_search.py # Contains the Page Object Model (POM) class │ ├─── drivers/ # Place your browser drivers here (e.g., msedgedriver.exe) │ ├─── reports/ # Test reports will be generated here │ ├─── screenshots/ # Directory for storing screenshots │ ├─── logs/ # Directory for storing logs │ ├─── report_generator.py # Module for custom report generation │ ├─── logger_config.py # Module for logging configuration │ ├─── requirements.txt # Python dependencies ├─── pytest.ini # Pytest configuration └─── README.md # Project documentation


## Installation

## **Clone the repository**:

   git clone <repository_url>
   cd automation_test_project

## **Create and activate a virtual environment**:
   python -m venv .venv
   Windows
   .venv\Scripts\activate
    macOS/Linux
   source .venv/bin/activate
## **Install required packages:**

pip install -r requirements.txt

## Download Microsoft Edge WebDriver 
place it in the drivers directory. Ensure the driver version matches your installed Edge browser version.

## Running Tests
To run the tests and generate an HTML report, execute the following command:
# pytest

## Viewing Reports
Navigate to the reports directory.
Open the test_report.html file in any web browser.
