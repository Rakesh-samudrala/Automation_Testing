from time import sleep
import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.page_search import SearchPage
from report_generator import generate_report, save_screenshot
from logger_config import setup_logger


@pytest.mark.usefixtures("webpage")
class TestSearchElement:

    @pytest.mark.parametrize(
        "product_name, is_existing_product",
        [
            ("ldsdfds15646846345tsdfdsfssfsdfxslfer", False),  # Non-existing product
            ("laptop", True),  # Existing product
        ]
    )
    def test_search_product(self, request, product_name, is_existing_product):
        # Set up logger specific to this test
        logger = setup_logger(request.node.name)

        search_page = SearchPage(self.driver)

        # Log the start of the test
        logger.info(f"Starting test for product: {product_name}")

        # Reload the page to ensure a fresh state before each test
        search_page.reload_page()

        # Search for the product (either existing or non-existing)
        search_page.search_product(product_name)

        # If it's an existing product, verify adding to the cart
        if is_existing_product:
            logger.info(f"Product {product_name} exists. Adding to cart.")
            # Scroll down to load more products
            search_page.scroll_down(pixels=500)

            # Add the product to the cart
            search_page.add_product_to_cart()

            # Wait for the cart confirmation and verify the product was added to the cart (1 in cart)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, search_page.cart_verification_xpath_template))
            )
            assert search_page.verify_cart_count(
                expected_count="1"), f"Product {product_name} was not added to the cart"
            logger.info(f"Product {product_name} added to the cart successfully.")

        # If it's a non-existing product, verify the "No results found" message
        else:
            logger.info(f"Checking for 'No results found' message for product: {product_name}")
            Empty = self.driver.find_element(By.XPATH, '//a[text()="Visit the help section"]').is_enabled()
            assert Empty, "True"
            logger.info(f"'No results found' message verified for {product_name}.")

        # Save a screenshot after test execution
        screenshot_path = save_screenshot(self.driver, request.node.name)

        # Generate report with logs and screenshots
        generate_report(request.node.name, True, screenshot_path, log_file=f"logs/{request.node.name}.log")

    def test_add_cart(self, request):
        # Set up logger specific to this test
        logger = setup_logger(request.node.name)

        search_page = SearchPage(self.driver)

        # Log the start of the test
        logger.info("Starting test to add product to cart.")

        # Scroll to the top of the page
        search_page.scroll_to_top()
        sleep(2)

        # Wait until the cart button is clickable and then click it
        logger.info("Clicking on the cart button.")
        cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, search_page.cart_button_id))
        )
        cart_button.click()

        # Wait for the cart page to load and get the quantity of items in the cart
        logger.info("Getting the quantity of items in the cart.")
        number = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, search_page.quantity_xpath))
        )
        amount = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@id='{search_page.subtotal_amount_id}']"))
        ).text
        con_amount = search_page.converter_int(amount)
        total = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, search_page.cart_subtotal_xpath))
        ).text
        con_total = search_page.converter_int(total)

        # Verify the amount and total match
        assert number.get_attribute("data-old-value") == '1' and con_amount == con_total, \
            "The amount and total do not match for a single item."

        logger.info("Verified that the amount and total match for a single item.")

        # Wait until the quantity dropdown is clickable, change to quantity 2
        logger.info("Changing quantity to 2.")
        dropdown_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//span[@class='a-button-text a-declarative'])[1]"))
        )
        dropdown_button.click()

        # Wait until the quantity dropdown option '2' is clickable, then select it
        quantity_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "quantity_2"))
        )
        quantity_option.click()

        # Wait for the updated quantity to reflect
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, search_page.quantity_xpath), "2")
        )

        # Verify the updated quantity and the updated total
        sleep(2)
        number = self.driver.find_element(By.XPATH, search_page.quantity_xpath)
        total = self.driver.find_element(By.XPATH, search_page.cart_subtotal_xpath).text
        con_total2 = search_page.converter_int(total)

        assert number.get_attribute("data-old-value") == '2' and con_total2 == con_amount * 2, \
            "The total is not correct according to the updated quantity."

        # Save screenshot after test execution
        screenshot_path = save_screenshot(self.driver, request.node.name)

        # Generate report with logs and screenshots
        generate_report(request.node.name, True, screenshot_path, log_file=f"logs/{request.node.name}.log")
