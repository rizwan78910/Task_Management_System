# tasks/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import date

class TaskModelTest(TestCase):
    
    def setUp(self):
        # Creating a user for task assignment
        self.user = User.objects.create_user(username='testuser', password='password')
    
    def test_task_creation(self):
        # Create a task instance
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        # Verify the task was created and is in the database
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.status, 'Pending')
        self.assertEqual(task.assigned_to, self.user)
    
    def test_str_method(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='In Progress',
            priority='High',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        # Verify the string representation of the task
        self.assertEqual(str(task), 'Test Task')
