from django.shortcuts import render, redirect
from django.http import HttpResponse

from todo.models import Item, List


def home_view(request):
    return render(request, 'todo/home.html')


def list_view(request, list_id):
    list_ = List.objects.get(id=list_id)

    return render(request, 'todo/list.html', {'list': list_})


def new_list_view(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['new_item'], list=list_)
    return redirect('lists', list_id=list_.pk)


def add_item_view(request, list_id):
    if request.method == 'POST':
        list_ = List.objects.get(id=list_id)
        item = Item.objects.create(text=request.POST['new_item'], list=list_)

        return redirect('lists', list_id=list_.pk)