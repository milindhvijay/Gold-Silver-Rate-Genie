import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
user_data_dir = os.getenv("USER_DATA_DIR")
phone_numbers_file_path = os.getenv("PHONE_NUMBERS_FILE_PATH")
rates_file_path = os.getenv("RATES_FILE_PATH")

with open(phone_numbers_file_path, 'r') as json_file:
    phone_numbers_data = json.load(json_file)
    phone_numbers = phone_numbers_data.get('phone_numbers', [])

with open(rates_file_path, 'r') as f:
    rates_message = f.read()

encoded_message = quote(rates_message)

# Initialize Chrome WebDriver with dedicated user data directory and in headless mode
options = webdriver.ChromeOptions()
options.add_argument(f'user-data-dir={user_data_dir}')
options.add_argument('--pageLoadStrategy=normal')  # Increase session timeout
# options.add_argument('--headless=new')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Send rates via WhatsApp
for number in phone_numbers:
    driver.get(f'https://web.whatsapp.com/send?phone={number}&text={encoded_message}')
    time.sleep(5)

    # screenshot_filename = f'screenshot_{number}.png'
    # driver.save_screenshot(screenshot_filename)

    driver.execute_script("window.onbeforeunload = null;")  # Prevent the unload event popup
    send_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="send"]')))
    send_button.click()

    time.sleep(5)

driver.quit()
