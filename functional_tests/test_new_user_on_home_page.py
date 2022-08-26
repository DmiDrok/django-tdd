from .base import FunctionalTest

from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from todo.models import List


class NewVisitorTest(FunctionalTest):
    def test_correct_items_for_diff_users(self):
        self.browser.get(self.live_server_url)

        self.send_keys_into_input('Купить продуктов')
        self.check_exist_item('Купить продуктов')
        
        self.browser.get(self.live_server_url)

        self.send_keys_into_input('Погладить футболку')
        self.check_exist_item('Погладить футболку')

        # URL от первого пользователя
        first_user_url = self.browser.current_url
        self.assertRegex(first_user_url, '/lists/.+')

        ## Начинаем тестировать нового пользователя
        self.browser.quit()

        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.browser.get(self.live_server_url)
        self.send_keys_into_input('Покормить рыбок')
        items = self.browser.find_elements(By.CLASS_NAME, 'item')

        self.assertTrue(all('Купить продуктов' not in item.text 
                        and 'Погладить футболку' not in item.text for item in items))
        
        second_user_url = self.browser.current_url
        print(second_user_url * 3, sep=' ')
        self.assertRegex(second_user_url, '/lists/.+')
        self.assertNotEqual(first_user_url, second_user_url)

    def test_correct_actions_on_the_forms(self):
        self.browser.get(self.live_server_url)

        form = self.browser.find_element(By.TAG_NAME, 'form')
        self.assertIn(reverse('home'), form.get_attribute('action').split(':')[1])

        list_ = List.objects.create()
        self.browser.get(self.live_server_url + reverse('lists', kwargs={'list_id': list_.pk}))
        form = self.browser.find_element(By.TAG_NAME, 'form')
        self.assertIn(reverse('home'), form.get_attribute('action').split(':')[1])
