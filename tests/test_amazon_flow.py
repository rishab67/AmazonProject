import pytest
from pages.search_page import SearchPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage

def test_amazon_search_flow(setup):
    driver = setup

    search_page = SearchPage(driver)
    results_page = SearchResultsPage(driver)
    product_page = ProductPage(driver)

    # Step 1: Search for product
    search_page.search_product("laptop")

    # Step 2: Apply filter
    results_page.apply_brand_filter("HP")

    # Step 3: Extract results (optional)
    results_page.extract_all_results(max_scrolls=2)

    # Step 4: Select first valid product
    results_page.select_first_product()

    # Step 5: Add to cart
    product_page.add_to_cart()
