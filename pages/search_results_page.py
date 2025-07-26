import time
import csv
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class SearchResultsPage:
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger if logger else self._get_default_logger()

    def _get_default_logger(self):
        logger = logging.getLogger("SearchResultsPage")
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)
        return logger

    def apply_brand_filter(self, brand_name):
        try:
            self.logger.info(f"Applying brand filter: {brand_name}")
            brand_xpath = f"//span[text()='{brand_name}']"
            brand_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, brand_xpath))
            )
            brand_element.click()
            # Wait for filter effect (page reload)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
            )
        except Exception as e:
            self.logger.error(f"Failed to apply brand filter: {e}")
            raise

    def select_first_product(self):
        try:
            self.logger.info("Selecting the first non-sponsored product")
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
                )
            )

            containers = self.driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
            print(f"DEBUG: Found {len(containers)} product containers")

            actions = ActionChains(self.driver)
            link_selectors = [
                "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal",
                "h2 a",
                "a.a-link-normal"
            ]

            for index, item in enumerate(containers, start=1):
                self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                time.sleep(0.2)

                # Skip sponsored
                try:
                    item.find_element(By.XPATH, ".//span[text()='Sponsored']")
                    print(f"DEBUG: Item {index} is sponsored → skipping")
                    continue
                except:
                    pass

                clicked = False
                for selector in link_selectors:
                    links = item.find_elements(By.CSS_SELECTOR, selector)
                    if links:
                        title = links[0].text
                        print(f"DEBUG: Clicking Item {index} using selector [{selector}]: {title}")
                        links[0].click()
                        clicked = True
                        break

                if clicked:
                    tabs = self.driver.window_handles
                    if len(tabs) > 1:
                        self.driver.switch_to.window(tabs[1])
                        print("DEBUG: Switched to new tab:", self.driver.title)
                    return

                print(f"DEBUG: Item {index} → No matching link for any selector")

            raise Exception("No valid product link found")
        except Exception as e:
            self.logger.error(f"Failed to select first product: {e}")
            raise

    def extract_all_results(self, max_scrolls=5, csv_file="amazon_results.csv"):
        try:
            self.logger.info("Extracting all product results with scrolling")
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
                )
            )

            product_data = []
            seen_links = set()

            for scroll_round in range(max_scrolls):
                self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(2)

                containers = self.driver.find_elements(
                    By.CSS_SELECTOR, "div[data-component-type='s-search-result']"
                )
                print(f"DEBUG: Scroll {scroll_round+1}: Found {len(containers)} containers")

                for item in containers:
                    try:
                        item.find_element(By.XPATH, ".//span[text()='Sponsored']")
                        continue
                    except:
                        pass

                    title_elem = item.find_elements(
                        By.CSS_SELECTOR,
                        "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal"
                    )
                    if not title_elem:
                        continue

                    title = title_elem[0].text
                    link = title_elem[0].get_attribute("href")

                    if link in seen_links:
                        continue
                    seen_links.add(link)

                    price_elem = item.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
                    price = price_elem[0].text if price_elem else "N/A"

                    product_data.append({"title": title, "price": price, "link": link})

            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
                writer.writeheader()
                writer.writerows(product_data)

            print(f"DEBUG: Saved {len(product_data)} products to {csv_file}")
            return product_data

        except Exception as e:
            self.logger.error(f"Failed to extract products: {e}")
            raise
