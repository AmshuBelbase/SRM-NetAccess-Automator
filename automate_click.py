# inbuilt imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os 

# Get the parent directory of the Python file being executed
parent_folder = os.path.dirname(os.path.abspath(__file__))


# private imports
from update_datetime import update_time
from get_current_ssid import get_wifi_ssid
from check_connection import check_connection
from post_ip import post_ip
from get_remote_ip import get_remote_ip
from read_lines import cred


# Get the current date and time
now = datetime.now()
print(now)


# get ssid
ssid = get_wifi_ssid()
print(f"Current SSID: {ssid}")

# headless
headless_mode = 1  # 0 - open chrome, 1 - Do not Open Chrome
credpath = f"{parent_folder}/cred.txt"

# check if element exists
def element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False


# if ssid is SRMIST -> check if internet is connected -> if no enter iach details on web -> again check internet

if (ssid == "SRMIST" or 1):
    print("Checking Internet ..")
    if not check_connection(headless_mode):
        print("Connected to Internet")
        update_time()
        lip = post_ip()
        rip = get_remote_ip()
        print("Local IP: ", lip)
        print("Retrieved from Firebase IP: ", rip)
    else:
        print("No Internet !! Starting Verification ..")

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

        urls = ["https://iac.srmist.edu.in/Connect/PortalMain", "https://iach.srmist.edu.in/Connect/PortalMain"]

        for url in urls:
            try:
                print("Opening WebPage", url)
                driver.get(url)
                print("Waiting to open", end=' ')
                for i in range(0, 3):
                    print(".", end=" ")
                    time.sleep(1)
                print()
                break

            except Exception as e: 
                print(e)

        try:
            red_flag = 0
            # Check if the username field exists before interacting
            if element_exists(driver, By.ID, "LoginUserPassword_auth_username"):
                print("Found Username Field!")
            else:
                red_flag = 1
                print("Username field not found!")

            # Check if the password field exists before interacting
            if element_exists(driver, By.ID, "LoginUserPassword_auth_password"):
                print("Found Password Field!")
            else:
                red_flag = 1
                print("Password field not found!")

            # Check if the login button field exists before interacting
            if element_exists(driver, By.ID, "UserCheck_Login_Button"):
                print("Found Username Field!")
            else:
                red_flag = 1
                print("Username field not found!")

            if not red_flag:
                # Get Credentials
                creds = cred(credpath) 

                # Find the username input field by its ID and type a value
                username_field = driver.find_element(
                    By.ID, "LoginUserPassword_auth_username")
                username_field.send_keys(creds[0])

                print("Typed into the username field successfully!")

                # Find the password input field by its ID and type a value
                psd_field = driver.find_element(
                    By.ID, "LoginUserPassword_auth_password")
                psd_field.send_keys(creds[1])

                print("Typed into the password field successfully!")

                login_button = driver.find_element(
                    By.ID, "UserCheck_Login_Button")

                # Ensure the button is visible by scrolling if necessary
                actions = ActionChains(driver)
                actions.move_to_element(login_button).click().perform()

                print("Login button clicked successfully!")

                # Wait for any potential redirects or actions
                time.sleep(2)

                print("Refreshing the page...")
                driver.refresh()

        except Exception as e:
            print(f"An error occurred: {e}")

        # Close the browser after a few seconds
        time.sleep(2)
        driver.quit()

        if not check_connection(headless_mode):
            print("Connected to Internet")
            update_time()
            lip = post_ip()
            rip = get_remote_ip()
            print("Local IP: ", lip)
            print("Retrieved from Firebase IP: ", rip)

        else:
            print("No Internet")
else:
    print("Connected to other network.")
    update_time()
    lip = post_ip()
    rip = get_remote_ip()
    print("Local IP: ", lip)
    print("Remote IP: ", rip)

# Get the current date and time
now = datetime.now()
print(now)
