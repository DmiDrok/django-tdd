from django.urls import path

from todo import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('lists/<int:list_id>/', views.list_view, name='lists'),
    path('lists/new', views.new_list_view, name='new_list'),
    path('lists/<int:list_id>/add_item', views.add_item_view, name='add_item'),
]