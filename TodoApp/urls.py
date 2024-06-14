from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('todo/<int:pk>/', views.todo_detail, name='todo_detail'),
    path('todo/new/', views.todo_create, name='todo_create'),
    path('todo/<int:pk>/edit/', views.todo_update, name='todo_update'),
    path('todo/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('todo/<int:todo_id>/complete/', views.todo_complete, name='todo_complete'),
    path('create-ec2/', views.create_ec2_instance, name='create_ec2'),
]
