import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import os
from logger_config import setup_logger

# Path to Edge WebDriver
service = Service(executable_path='drivers/msedgedriver.exe')

@pytest.fixture(scope="class")
def webpage(request):
    # Set up logger specific to the test class
    logger = setup_logger(request.node.name)
    logger.info("Initializing Edge WebDriver")

    # Initialize WebDriver
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    driver.implicitly_wait(5)

    # Open Amazon website and log the action
    logger.info("Opening Amazon.in")
    driver.get("https://www.amazon.in")

    request.cls.driver = driver  # Assign driver to test class

    yield

    # Teardown, log the action, and close the browser
    logger.info("Closing the WebDriver")
    driver.quit()

def pytest_runtest_makereport(item, call):
    """Attach screenshot to the report on failure."""
    if call.when == "call" and call.excinfo is not None:
        screenshot_path = os.path.join("screenshots", f"{item.name}.png")
        if os.path.exists(screenshot_path):
            # Attach the screenshot to the report
            item.user_properties.append(("screenshot", screenshot_path))
