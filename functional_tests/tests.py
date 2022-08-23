from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from todo.models import Item

from time import sleep

import os
import unittest
import time


MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    driver_path = os.path.join('drivers', 'chromedriver.exe')

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=self.driver_path)

    def tearDown(self):
        self.browser.quit()

    def send_keys_to_input(self, keys):
        input_new_item = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')
        
        input_new_item.send_keys(keys)
        input_new_item.send_keys(Keys.ENTER)

    def is_keys_in_page(self, keys):
        start_time = time.time()
        while True:
            try:
                items = self.browser.find_elements(By.CLASS_NAME, 'item')
                self.assertTrue(any(keys in item.text for item in items))
                return
            except Exception as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                
                time.sleep(0.5)

    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('To-Do', header.text)

        self.send_keys_to_input('Погладить одежду')
        self.send_keys_to_input('Подоить корову')

        self.browser.get(self.live_server_url + reverse('lists', kwargs={'list_id': 1}))
        self.is_keys_in_page('Погладить одежду')
        self.is_keys_in_page('Подоить корову')

        # Проверяем url адрес по шаблону
        current_url_first_user = self.browser.current_url
        self.assertRegex(current_url_first_user, r'/lists/.*')
        
        ## Тестируем нового пользователя
        self.browser.quit()
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.browser.get(self.live_server_url)
        items = self.browser.find_elements(By.CLASS_NAME, 'item')
        self.assertTrue(all('Погладить одежду' != item.text for item in items))
        self.assertTrue(all('Подоить корову' != item.text for item in items))

        # Проверяем уникальность url-адреса первого и второго пользователей
        current_url_second_user = self.browser.current_url
        self.assertNotEqual(current_url_first_user, current_url_second_user)

    def test_layout_and_styling(self):
        # Андрей заходит на главную страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # На главной странице он видит input-поле, расположенное посередине
        inputbox = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10,
        )

        inputbox.send_keys('Помыть кота')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.browser.find_element(By.CLASS_NAME, 'add_new_item_inp')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10,
        )

