import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def setup(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.amazon.in")

    yield driver

    # Capture screenshot if test fails
    if request.node.rep_call.failed:
        screenshots_dir = os.path.join("reports")
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, f"failure_{request.node.name}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

    driver.quit()

# Hook for pytest to detect test failures
def pytest_runtest_makereport(item, call):
    if "setup" in item.fixturenames:
        item._store = getattr(item, "_store", {})
        if call.when == "call":
            item._store["rep_call"] = call

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
