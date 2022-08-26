from .base import FunctionalTest

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class CorrectLayoutAndStylingTest(FunctionalTest):
    def test_correct_title_and_header(self):
        self.browser.get(self.live_server_url)
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertTrue(any('To-Do' in element for element in [self.browser.title, header.text]))

    def test_correct_layout_and_styling(self):
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=50,
        )
