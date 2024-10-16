import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_report_directory():
    """Create a report directory if it doesn't exist."""
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    return report_dir


def generate_report(test_name, success, screenshot_path=None, log_file=None):
    """Generate a custom report for the test in HTML format."""
    report_dir = create_report_directory()
    report_file = os.path.join(report_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

    # Read logs from the specified log file
    logs = ""
    if log_file and os.path.exists(log_file):
        with open(log_file, 'r') as log_file_handle:
            logs = log_file_handle.read()

    with open(report_file, 'w') as f:
        # Write HTML headers and title
        f.write("<html>\n<head>\n<title>Test Report</title>\n</head>\n<body>\n")
        f.write(f"<h1>Test Name: {test_name}</h1>\n")
        f.write(f"<p>Status: {'Passed' if success else 'Failed'}</p>\n")

        if screenshot_path:
            # Use relative path for the screenshot
            relative_screenshot_path = os.path.relpath(screenshot_path, report_dir)
            f.write(f"<p>Screenshot:</p>\n")
            f.write(f'<img src="{relative_screenshot_path}" alt="Screenshot" style="max-width:600px;">\n')

        # Add logs to the report
        f.write("<h2>Logs:</h2>\n")
        f.write("<pre>\n")  # Start preformatted text block
        f.write(logs)
        f.write("</pre>\n")

        f.write("</body>\n</html>")

    logging.info(f"HTML report generated: {report_file}")


def save_screenshot(driver, test_name):
    """Utility function to save a screenshot."""
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)  # Create directory if it doesn't exist
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
    driver.save_screenshot(screenshot_path)
    logging.info(f"Screenshot saved at: {screenshot_path}")
    return screenshot_path
