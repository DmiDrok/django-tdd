from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse

from todo.models import Item, List


def home_view(request):
    error = None

    if request.method == 'POST':
        list_ = List.objects.create()
        try:
            item = Item.objects.create(text=request.POST['new_item'], list=list_)
            item.full_clean()

            return redirect(list_)
        except ValidationError:
            list_.delete()
            error = 'Введите задание. Запрещено вводить пустую строку.'

    return render(request, 'todo/home.html', {'error': error})


def list_view(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['new_item'], list=list_)
            item.full_clean()
            item.save()

            return redirect(list_)
        except ValidationError:
            error = 'Введите задание. Запрещено вводить пустую строку.'


    return render(request, 'todo/list.html', {'list': list_, 'error': error})
