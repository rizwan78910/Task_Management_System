from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User  # Use the default User model
from django.contrib.auth.forms import UserCreationForm  # Use the built-in form

# Task list view with optional filters
@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    if request.user.is_superuser:
        tasks = Task.objects.all()  # Admin sees all tasks
    else:
        tasks = Task.objects.filter(assigned_to=request.user)  # Users see only their tasks

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


# Create a new task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to task list after saving
    else:
        form = TaskForm()
    
    return render(request, 'tasks/create_task.html', {'form': form})


# Edit an existing task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect after saving
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/edit_task.html', {'form': form})


# Delete an existing task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')  # Redirect after deletion


# Create User using the built-in UserCreationForm
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the user and password correctly
            messages.success(request, "User created successfully!")
            return redirect('view_users')  # Redirect to the user list or a relevant page
        else:
            messages.error(request, "There was an error creating the user.")
    else:
        form = UserCreationForm()

    return render(request, 'tasks/create_user.html', {'form': form})


# View Users
def view_users(request):
    users = User.objects.all()  # Use the default User model
    return render(request, 'tasks/view_users.html', {'users': users})


# Login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # Use username for authentication

        if user is not None:
            login(request, user)
            return redirect("task_list")  # Redirect to task list after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "tasks/login.html")



from django.shortcuts import render

def request_account_view(request):
    return render(request, 'tasks/request_account.html')

