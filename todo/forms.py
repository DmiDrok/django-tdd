from django import forms

from .models import Item


EMPTY_ITEM_ERROR = 'Введите задание. Запрещено вводить пустую строку.'
DUPLICATE_ITEM_ERRORS = 'Такое задание уже есть.'
class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['text']
        widgets = {
            'text': forms.TextInput({'placeholder': 'Введи задачу',
                                     'class': 'add_new_item_inp',})
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_unique(self):
        try:
            self.validate_unique()
        except Exception as e:
            self.add_error('text', DUPLICATE_ITEM_ERRORS)

    def save(self):
        return forms.ModelForm.save(self)