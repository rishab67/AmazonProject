from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.XPATH, "//input[@id='twotabsearchtextbox']")
        self.search_button = (By.XPATH, "//input[@id='nav-search-submit-button']")

    def search_product(self, product_name):
        self.driver.find_element(*self.search_box).clear()
        self.driver.find_element(*self.search_box).send_keys(product_name)
        self.driver.find_element(*self.search_button).click()
