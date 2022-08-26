from django.test import TestCase
from django.urls import  reverse
from django.core.exceptions import ValidationError

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
    
    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), reverse('lists', kwargs={'list_id': list_.pk}))
