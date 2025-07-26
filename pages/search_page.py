import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger if logger else self._get_default_logger()

    def _get_default_logger(self):
        logger = logging.getLogger("SearchPage")
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)
        return logger

    def search_product(self, product_name):
        self.logger.info("Locating search box")
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.clear()
        search_box.send_keys(product_name)
        self.logger.info(f"Entered search term: {product_name}")

        search_button = self.driver.find_element(By.ID, "nav-search-submit-button")
        self.logger.info("Clicking search button")
        search_button.click()
