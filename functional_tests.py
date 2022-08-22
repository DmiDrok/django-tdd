from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    driver_path = os.path.join('drivers', 'chromedriver.exe')

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=self.driver_path)

    def tearDown(self):
        self.browser.quit()

    def is_item_in_page(self, it, items):
        self.assertTrue(any(it in item.text for item in items))

    def send_keys_to_input(self, keys):
        input_new_item = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')
        
        input_new_item.send_keys(keys)
        input_new_item.send_keys(Keys.ENTER)

    def is_keys_in_page(self, keys):
        items = self.browser.find_elements(By.CLASS_NAME, 'item')
        self.assertTrue(any(keys in item.text for item in items))

    def test_home_page(self):
        self.browser.get('http://localhost:8000/')
        self.assertIn('To-Do', self.browser.title)

        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('To-Do', header.text)

        self.send_keys_to_input('Погладить одежду')
        self.send_keys_to_input('Подоить корову')

        self.is_keys_in_page('Погладить одежду')
        self.is_keys_in_page('Подоить корову')


if __name__ == "__main__":
    unittest.main()