from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .views import view_users
from .views import create_user

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Login view
    path('', views.task_list, name='task_list'),
    path('create-task/', views.create_task, name='create_task'),  # Unique path for creating task
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('create-user/', views.create_user, name='create_user'),
    path('view-users/', view_users, name='view_users'),
    path('request_account/', views.request_account_view, name='request_account'),
    
]
