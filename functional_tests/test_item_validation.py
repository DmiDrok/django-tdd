from .base import FunctionalTest

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ItemValidationTest(FunctionalTest):
    def test_correct_empty_item_response(self):
        self.browser.get(self.live_server_url)
        input_field = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')

        input_field.send_keys('')
        input_field.send_keys(Keys.ENTER)

        items = self.browser.find_elements(By.CLASS_NAME, 'item')
        warning_block = self.browser.find_element(By.CLASS_NAME, 'has_error')

        self.assertEqual(len(items), 0)
        self.wait_for(lambda: 'запрещено' in self.browser.find_element(By.CLASS_NAME, 'has_error').text)
