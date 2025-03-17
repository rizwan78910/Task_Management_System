from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Function to redirect root URL to 'login/'
def redirect_to_login(request):
    return redirect('login')

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('login')


urlpatterns = [
    path('', redirect_to_login, name='home'),  # Redirect root URL to 'login/'
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    
    
]
