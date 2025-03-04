from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# Task list view with optional filters
@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    tasks = Task.objects.all()

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
