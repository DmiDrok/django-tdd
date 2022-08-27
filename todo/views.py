from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse

from todo.models import Item, List
from todo.forms import ExistingListItemForm, ItemForm


def home_view(request):
    form = ExistingListItemForm(request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)

        return redirect(list_)
    
    return render(request, 'todo/home.html', {'form': form})


def list_view(request, list_id):
    list_ = List.objects.get(pk=list_id)
    form = ExistingListItemForm()

    if request.method == 'POST':
        form = ExistingListItemForm(request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)

    return render(request, 'todo/list.html', {'list': list_, 'form': form})
