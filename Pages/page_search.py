from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:
    def __init__(self, driver):
        self.driver = driver

        # Define locators
        self.search_bar_id = 'twotabsearchtextbox'
        self.search_button_id = 'nav-search-submit-button'
        self.add_to_cart_button_xpath = '(//button[contains(@id,"a-autoid-")])[4]'
        self.cart_verification_xpath_template = "//div[@class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_4']//span[@class='a-size-mini a-color-secondary puis-atcb-remove-group-message a-text-bold'][normalize-space()='1 in cart']"
        self.no_results_xpath = "//span[contains(text(),'No results')]"
        self.cart_button_id = "nav-cart"
        self.quantity_xpath = "//span[@class='sc-action-quantity']"
        self.subtotal_amount_id = "sc-subtotal-amount-buybox"
        self.cart_subtotal_xpath = '//*[@id="sc-subtotal-amount-buybox"]/span'

    def search_product(self, product_name):
        """Search for a product using the search bar."""
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.search_bar_id))
        )
        search_bar.clear()
        search_bar.send_keys(product_name)

        # Click on the search button
        search_button = self.driver.find_element(By.ID, self.search_button_id)
        search_button.click()

    def reload_page(self):
        """Reload the Amazon homepage to reset the state."""
        self.driver.get("https://www.amazon.in")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, self.search_bar_id))
        )

    def scroll_down(self, pixels=500):
        """Scroll down the page by a specified number of pixels."""
        self.driver.execute_script(f"window.scrollTo(0, {pixels});")

    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def add_product_to_cart(self):
        """Click on the add to cart button."""
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.add_to_cart_button_xpath))
        )
        add_to_cart_button.click()

    def verify_cart_count(self, expected_count):
        """Verify if the cart has the correct quantity of items."""
        cart_verification_xpath = self.cart_verification_xpath_template
        cart_count_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, cart_verification_xpath))
        )
        return cart_count_element.is_displayed()

    def no_results_found(self):
        """Check if a 'No results found' message is displayed for a non-existing product."""
        try:
            no_results_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.no_results_xpath))
            )
            return no_results_element.is_displayed()
        except:
            return False

    def converter_int(self, value):
        """Convert a formatted string to an integer."""
        value = value.strip().replace(',', '')  # Remove commas
        return int(float(value))  # Convert to float then to int
