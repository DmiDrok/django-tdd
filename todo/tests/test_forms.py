from django.test import TestCase
from django.urls import reverse

from ..forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERRORS, ItemForm, ExistingListItemForm
from ..models import Item, List


class ItemFormTestCase(TestCase):
    def test_forms_render(self):
        form = ItemForm()
        self.assertIn('placeholder="Введи задачу"', form.as_p())
        self.assertIn('class="add_new_item_inp"', form.as_p())

    def test_form_validations_for_the_blank(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR ])

    def test_correct_save_data_form(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'Задача'})
        form.save(for_list=list_)
        new_item = Item.objects.first()
        item_db = Item.objects.first()

        self.assertEqual(new_item, item_db)
        self.assertEqual(new_item.text, 'Задача')
        self.assertEqual(new_item.list, list_)

    def test_form_validation_on_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Задача 1', list=list_)
        form = ExistingListItemForm(for_list=list_, data={'text': 'Задача 1'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERRORS])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'Задача 1'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())

