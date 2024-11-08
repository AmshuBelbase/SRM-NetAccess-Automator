# pi@raspberrypi:~ $ whereis chromedriver
# chromedriver: /usr/bin/chromedriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# headless
# headless_mode = 1  # 0 - open chrome, 1 - Do not Open Chrome


def element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False


def check_connection(headless_mode):
    try:
        # Set Chrome options for headless mode
        chrome_options = Options()
        if headless_mode:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--window-size=1920,1080")

        # Specify the ChromeDriver service
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        url = "https://facebook.com"
        print("Opening test site", end=' ')
        driver.get(url)
        err_flag = 0

        for i in range(1, 4):
            print(".", end=' ')
            time.sleep(1)

        print(".")
        # Check for an example element
        if element_exists(driver, By.NAME, "email"):
            print("Smaple input field found!")
        else:
            print("Sample input field not found!")

        print("\nClosing Test Site")
        time.sleep(1)

        # Close the browser
        driver.quit()

    except Exception as e:
        err_flag = 1
        print(e)

    return err_flag


if __name__ == "__main__":
    if not check_connection(headless_mode=1):
        print("Connected to Internet")
    else:
        print("No Internet")
