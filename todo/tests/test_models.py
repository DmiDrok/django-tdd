from django.test import TestCase
from django.urls import  reverse
from django.core.exceptions import ValidationError

from todo.models import Item, List


class ListsItemModelTest(TestCase):
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text='Задача 1', list=list_)
        item2 = Item.objects.create(text='Задача 2', list=list_)
        item3 = Item.objects.create(text='Задача 3', list=list_)

        self.assertIn(item1, list_.item_set.all())

    
    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(text='', list=list_)

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), reverse('lists', kwargs={'list_id': list_.pk}))

    def test_cannot_add_duplicate_items(self):
        list_ = List.objects.create()
        item_first = Item.objects.create(text='Задача 1', list=list_)

        with self.assertRaises(ValidationError):
            item_second = Item(text='Задача 1', list=list_)
            item_second.full_clean()