import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.search_page import SearchPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_basic_search(setup):
    driver = setup
    page = SearchPage(driver)

    page.enter_search_term("laptop")
    page.click_search_button()

    # Wait until at least one product appears
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
    )

    # Debugging: print title
    print("TITLE BEFORE WAIT:", driver.title)

    # Wait until title is non-empty
    WebDriverWait(driver, 10).until(lambda d: d.title.strip() != "")

    print("TITLE AFTER WAIT:", driver.title)

    assert "laptop" in driver.title.lower()
