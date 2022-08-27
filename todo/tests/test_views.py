from django.test import TestCase
from django.urls import reverse, resolve

from ..models import List, Item
from ..views import home_view
from ..forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERRORS, ItemForm, ExistingListItemForm


class NewItemTest(TestCase):
    def test_redirect_after_post_request(self):
        response = self.client.post(reverse('home'), data={'text': 'Новая задача'})
        list_ = List.objects.first()
        self.assertRedirects(response, reverse('lists', kwargs={'list_id': list_.pk}))

    def test_can_save_after_post_request(self):
        response = self.client.post(reverse('home'), data={'text': 'Задача 1'})
        self.assertEqual(Item.objects.count(), 1)

    def test_can_assign_with_exist_list(self):
        list_ = List.objects.create()

        response = self.client.post(reverse('lists', kwargs={'list_id': list_.pk}), data={'text': 'Помыть кота'})
        item = Item.objects.get(list=list_)

        self.assertEqual(item.text, 'Помыть кота')
        self.assertEqual(item.list, list_)

    def test_redirects_after_add_in_exist_list(self):
        current_list = List.objects.create()
        response = self.client.post(reverse('lists', kwargs={'list_id': current_list.pk}), data={'text': 'Новая задачка'})

        self.assertRedirects(response, reverse('lists', kwargs={'list_id': current_list.pk}))

    def test_error_on_empty_item(self):
        response = self.client.post(reverse('home'), data={'text': ''})
        self.assertEqual(response.status_code, 200)

    def test_error_on_empty_item_add_in_exist_list(self):
        list_ = List.objects.create()
        response = self.client.post(reverse('lists', kwargs={'list_id': list_.pk}), data={'text': ''})
        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_correct_form_is_using_in_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_empty_item_not_add_in_db(self):
        response = self.client.post(reverse('home'), data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class HomePageTest(TestCase):
    def test_correct_view_works_on_url(self):
        works = resolve(reverse('home'))
        self.assertEqual(works.func, home_view)

    def test_correct_template_on_url(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'todo/home.html')


class ListsViewTest(TestCase):
    def test_correct_template_on_url(self):
        list_ = List.objects.create()

        response = self.client.get(reverse('lists', kwargs={'list_id': list_.pk}))
        self.assertTemplateUsed(response, 'todo/list.html')

    def test_display_only_correct_list(self):
        correct_list = List.objects.create()
        second_list = List.objects.create()
        item1 = Item.objects.create(text='Задача первого списка', list=correct_list)
        item2 = Item.objects.create(text='Задача второго списка', list=second_list)

        response = self.client.get(reverse('lists', kwargs={'list_id': correct_list.pk}))
        html = response.content.decode('utf-8')

        self.assertIn(item1.text, html)
        self.assertNotIn(item2.text, html)

    def test_correct_list_into_page(self):
        current_list = List.objects.create()
        response = self.client.get(reverse('lists', kwargs={'list_id': current_list.pk}))

        self.assertEqual(response.context['list'], current_list)


