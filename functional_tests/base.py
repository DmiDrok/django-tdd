from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException

import os
import time


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    driver_path = os.path.join('drivers', 'chromedriver.exe')

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.browser.set_window_size(1024, 768)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def send_keys_into_input(self, keys: str):
        input_field = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')
        input_field.send_keys(keys)
        input_field.send_keys(Keys.ENTER)

    def check_exist_item(self, it: str):
        start = time.time()
        while True:
            try:
                items = self.browser.find_elements(By.CLASS_NAME, 'item')
                self.assertTrue(any(it in item.text for item in items))
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e

            time.sleep(0.5)

    def wait_for(self, fn):
        start = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e

            time.sleep(0.5)
