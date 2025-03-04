from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'due_date')  # Customize displayed columns
    list_filter = ('status', 'assigned_to', 'due_date')  # Add filters
    search_fields = ('title', 'description')  # Enable search functionality
    ordering = ('due_date',)  # Sort tasks by due date

admin.site.register(Task, TaskAdmin)
