import os
import time
import logging
import pytest
# from pages.search_page import SearchPage
# from pages.search_results_page import SearchResultsPage
# from pages.product_page import ProductPage
from AmazonProject.pages.search_page import SearchPage
from AmazonProject.pages.search_results_page import SearchResultsPage
from AmazonProject.pages.product_page import ProductPage


# === Configure Logging ===
os.makedirs("reports", exist_ok=True)
log_file = os.path.join("reports", "test_log.txt")
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AmazonTest")

@pytest.mark.usefixtures("setup")
def test_amazon_search_flow(setup):
    driver = setup
    search_page = SearchPage(driver, logger)
    results_page = SearchResultsPage(driver, logger)
    product_page = ProductPage(driver, logger)

    try:
        # Step 1: Search product
        logger.info("Step 1: Searching for laptops...")
        search_page.search_product("laptop")

        # Step 2: Apply brand filter
        logger.info("Step 2: Applying HP filter...")
        results_page.apply_brand_filter("HP")

        # Step 3: Extract results
        logger.info("Step 3: Extracting search results...")
        results_page.extract_all_results(max_scrolls=2)

        # Step 4: Select first product
        logger.info("Step 4: Selecting first valid product...")
        results_page.select_first_product()

        # Step 5: Add to cart
        logger.info("Step 5: Adding product to cart...")
        added = product_page.add_to_cart()
        assert added, "Add to Cart failed"
        logger.info("✅ Product successfully added to cart.")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

        # Capture screenshot
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join("reports", f"failure_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved: {screenshot_path}")

        # Re-raise to mark the test as failed
        raise
