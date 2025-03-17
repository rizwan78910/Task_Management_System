# tasks/tests/test_forms.py
from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import Task
from django.contrib.auth.models import User
from datetime import date

class TaskFormTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
    
    def test_task_form_valid(self):
        form_data = {
            'title': 'Valid Task',
            'description': 'Description for valid task',
            'status': 'Pending',
            'priority': 'Medium',
            'due_date': date.today(),
            'assigned_to': self.user.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_task_form_invalid(self):
        form_data = {
            'title': '',  # Missing title
            'description': 'Description for invalid task',
            'status': 'Pending',
            'priority': 'Medium',
            'due_date': date.today(),
            'assigned_to': self.user.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

