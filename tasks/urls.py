from django.contrib.auth.views import LoginView  # Add this import
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Login view
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]