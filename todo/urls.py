from django.urls import path

from todo import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('lists/<int:list_id>/', views.list_view, name='lists'),
]