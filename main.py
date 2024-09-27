"""
This script opens instagram, logs in using a proxy, and then iterates through a list of usernames.
For each username, it opens their profile, waits for the page to load, gets the image source of their profile picture,
gets a description of the image using an AI model, and then sends a message to the user using the AI-generated description.
"""

import json
import sys
import os
import time
import uuid

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.AI.get_AI_greeting_handler import get_AI_greeting_handler
from src.AI.get_image_description import get_image_description
from src.GLOBAL import GLOBAL
from src.database.database import Session, Account
from src.driver.driver import BaseSeleniumDriver
from src.proxy import Proxy
from src.utils.bot.bot_humanity import random_sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

load_dotenv()
current_proxy = os.getenv('current_proxy')



BASE_URL = 'https://instagram.com/'
session = Session()
account = session.query(Account).filter(Account.account_name == 'Account').first()
if account is None:
    print('Account not found. Login first into instagram.')
    driver = BaseSeleniumDriver(
        executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH,
        headless=False,
        window_size=(1280, 720),
    )
    driver.create_instance()
    driver.get(BASE_URL + '/direct/inbox/')
    print("Please wait for setup...")
    time.sleep(10)
    while 'https://www.instagram.com/accounts/login/' in driver.current_url:
        print("Please Login into instagram")
        time.sleep(10)
    cookie = driver.get_cookies()
    cookie_json = json.dumps(cookie)
    account = Account(uuid=str(uuid.uuid4()),account_name='Account', cookies=cookie_json)
    session.add(account)
    session.commit()
    driver.quit()
    account = session.query(Account).filter(Account.account_name == 'Account').first()
    print('Account created.')


driver = BaseSeleniumDriver(
    executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH,
    headless=False,
    window_size=(1280, 720),
    proxy=Proxy.from_user_format_string(current_proxy)
)
user_names = []

with open('instagram_accounts.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            user_names.append(line)


driver.create_instance()
driver.set_page_load_timeout(120)

driver.get(BASE_URL)
time.sleep(10)

# clear cookies
driver.delete_all_cookies()
cookies = json.loads(account.cookies)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
print('Cookies loaded')
try:
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click()
except TimeoutException as e:
    pass

"""
This loop iterates through the list of usernames and:
1. Opens the profile of each username.
2. Waits for the page to load.
3. Gets the image source of the user's profile picture.
4. Gets a description of the image using an AI model.
5. Sends a message to the user using the AI-generated description.
"""

for user_name in user_names:
    driver.set_page_load_timeout(120)
    driver.get(BASE_URL + user_name)
    # waiting for page to load using bs4
    try:
        WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='link']//img"))
        )
    except Exception as ex:
        print(ex)
        continue
    page_source = driver.page_source
    # get image source by xpath //div[@role='button']//span[@role='link']//img using selenium
    soup = BeautifulSoup(page_source, 'html.parser')
    image_source = ''
    try:

        image_source_element = driver.find_element(By.XPATH, "//span[@role='link' and @style='height: 150px; width: "
                                                             "150px;']//img[@crossorigin='anonymous']")
        image_source = image_source_element.get_attribute('src')

    except Exception as ex:
        image_source_element = driver.find_element(By.XPATH, "//img[@crossorigin='anonymous' and contains(@alt, "
                                                             "'profile picture')]")
        image_source = image_source_element.get_attribute('src')

    if not image_source:
        print('image source not found', user_name)
        continue
    try:
        message_button = driver.find_element(By.XPATH, "//div[text()='Message']")
        print(message_button, "data type: ", type(message_button))
        message_button.click()
    except NoSuchElementException as ex:
        try:
            options_button = driver.find_element(By.XPATH, "//*[@aria-label='Options']")
            options_button.click()
            random_sleep(2, 5)
            message_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Send message')]")
            message_button.click()
        except NoSuchElementException as ex:
            print(f'Except exception no such element: {ex}')
            continue
    except Exception as ex:
        print(f'Except exception: {ex}')
    try:
        wait = WebDriverWait(driver, 10)
        # Wait for the alert element to be present
        alert = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='alert']")))
        # Now you can interact with the alert element
        print("Alert found:", alert.text)
    except TimeoutException:
        print("Alert did not appear within the given time.")

    # get description using AI model
    ai_description = get_image_description(image_source)
    print(ai_description, '*' *20)
    if not ai_description:
        print('AI description not found')
        continue
    message = get_AI_greeting_handler(ai_description).strip('"')

    print(message)
    if not message:
        print('AI message not found')
        continue

    random_sleep(0.5, 1.5)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Message']"))).click()
    except TimeoutException:
        continue

    message_box = driver.find_element(By.XPATH, "//div[@aria-label='Message']")
    message_box.click()
    message_box.clear()
    # huminity typing (to not detect)
    for i in message:
        try:
            message_box.send_keys(f'{i}')
            random_sleep(0.2, 0.5)
        except Exception as ex:
            print(f'Exception element gone: {ex}')
            break

    message_box.send_keys('\n')
    random_sleep(4, 6)

    print(f'{user_name} - {image_source}')


driver.quit()