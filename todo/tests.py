from django.test import TestCase
from django.urls import resolve, reverse

from todo.views import home_view
from todo.models import Item, List


class ListsItemModelTest(TestCase):
    def test_save_and_assign_both(self):
        list_ = List()
        list_.save()

        item1 = Item(text='Задача 1')
        item2 = Item(text='Задача 2')

        item1.list = list_
        item2.list = list_
        item1.save()
        item2.save()

        self.assertEqual(item1.list, list_)
        self.assertEqual(item2.list, list_)


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


class NewItemTest(TestCase):
    def test_redirect_after_post_request(self):
        response = self.client.post(reverse('new_list'), data={'new_item': 'Новая задача'})
        list_ = List.objects.first()
        self.assertRedirects(response, reverse('lists', kwargs={'list_id': list_.pk}))

    def test_can_save_after_post_request(self):
        response = self.client.post(reverse('new_list'), data={'new_item': 'Задача 1'})
        self.assertEqual(Item.objects.count(), 1)

    def test_can_assign_with_exist_list(self):
        list_ = List.objects.create()

        response = self.client.post(reverse('add_item', kwargs={'list_id': list_.pk}), data={'new_item': 'Помыть кота'})
        item = Item.objects.get(list=list_)

        self.assertEqual(item.text, 'Помыть кота')
        self.assertEqual(item.list, list_)

    def test_redirects_after_add_in_exist_list(self):
        current_list = List.objects.create()
        second_list = List.objects.create()

        response = self.client.post(reverse('add_item', kwargs={'list_id': current_list.pk}), data={'new_item': 'Новая задачка'})

        self.assertRedirects(response, reverse('lists', kwargs={'list_id': current_list.pk}))


class HomePageTest(TestCase):
    def test_correct_view_works_on_url(self):
        works = resolve(reverse('home'))
        self.assertEqual(works.func, home_view)

    def test_correct_template_on_url(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'todo/home.html')
