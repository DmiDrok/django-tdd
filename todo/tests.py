from django.test import TestCase
from django.urls import resolve, reverse

from todo.views import home_view
from todo.models import Item


class ItemModelTest(TestCase):
    def test_item_model(self):
        Item.objects.create(text='Задача 1')
        Item.objects.create(text='Задача 2')

        self.assertEqual(Item.objects.count(), 2)


class HomePageTest(TestCase):
    def test_correct_view_works_on_url(self):
        works = resolve(reverse('home'))
        self.assertEqual(works.func, home_view)

    def test_correct_template_on_url(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'todo/home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post(reverse('home'), data={'new_item': 'Задачка'})
        self.assertEqual(Item.objects.count(), 1)

    def test_correct_display_on_page(self):
        item_1 = Item.objects.create(text='Задача 1')
        item_2 = Item.objects.create(text='Задача 2')

        response = self.client.get(reverse('home'))
        html = response.content.decode('utf-8')

        self.assertIn(item_1.text, html)
        self.assertIn(item_2.text, html)

    def test_redirect_after_post_request(self):
        response = self.client.post('/', data={'new_item': 'Новое дело'})

        self.assertEqual(response['location'], '/')
        self.assertEqual(response.status_code, 302)