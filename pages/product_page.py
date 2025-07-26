import logging
import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger if logger else self._get_default_logger()

    def _get_default_logger(self):
        logger = logging.getLogger("ProductPage")
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)
        return logger

    def add_to_cart(self):
        try:
            wait = WebDriverWait(self.driver, 10)

            # Scroll & click standard Add to Cart
            try:
                add_button = wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-button")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", add_button)
                self.logger.info("Clicked standard Add to Cart button.")
            except TimeoutException:
                self.logger.warning("Standard Add to Cart button not found. Trying fallbacks...")

                # Try Buying Options
                try:
                    see_options = wait.until(
                        EC.element_to_be_clickable((By.ID, "buybox-see-all-buying-choices-announce"))
                    )
                    see_options.click()
                    add_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit.addToCart")))
                    self.driver.execute_script("arguments[0].click();", add_button)
                    self.logger.info("Added to cart via Buying Options.")
                except TimeoutException:
                    # Try popup/side cart
                    try:
                        proceed_cart = wait.until(
                            EC.element_to_be_clickable((By.ID, "attach-view-cart-button-form"))
                        )
                        self.driver.execute_script("arguments[0].click();", proceed_cart)
                        self.logger.info("Added to cart using popup cart.")
                    except TimeoutException:
                        self.logger.error("No Add to Cart option found.")
                        return False

            # ✅ Now verify cart confirmation
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h1[contains(text(),'Added to Cart')] | //span[contains(text(),'Added to Cart')]")
                    )
                )
                self.logger.info("Confirmed: Product was added to cart.")
                return True
            except TimeoutException:
                self.logger.warning("No 'Added to Cart' message. Taking screenshot...")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"reports/failure_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                self.logger.error(f"Screenshot saved: {screenshot_path}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to add to cart: {e}")
            return False
