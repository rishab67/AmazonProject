import logging
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
            self.logger.info("Attempting to add product to cart")
            add_to_cart_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
            )
            add_to_cart_btn.click()
            self.logger.info("Product added to cart successfully")
        except Exception as e:
            self.logger.error(f"Failed to add to cart: {e}")
            raise
