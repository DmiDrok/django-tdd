from django.shortcuts import render, redirect

from todo.models import Item


def home_view(request):
    all_items = Item.objects.all()
    
    if request.method == 'POST':
        Item.objects.create(text=request.POST['new_item'])
        return redirect('/')

    return render(request, 'todo/home.html', {'all_items': all_items})

