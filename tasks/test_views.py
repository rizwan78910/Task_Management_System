# tasks/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import date

class TaskViewsTest(TestCase):
    
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
    
    def test_task_list_view(self):
        # Create tasks for the user
        Task.objects.create(
            title='Test Task 1',
            description='Description 1',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        Task.objects.create(
            title='Test Task 2',
            description='Description 2',
            status='Completed',
            priority='High',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')
    
    def test_create_task_view(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Task')

        # Submitting the form to create a new task
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'Description of new task',
            'status': 'Pending',
            'priority': 'Medium',
            'due_date': date.today(),
            'assigned_to': self.user.id,
        })
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 1)
    
    def test_edit_task_view(self):
        # Create a task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        response = self.client.get(reverse('edit_task', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Task')
        
        # Edit the task
        response = self.client.post(reverse('edit_task', args=[task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'In Progress',
            'priority': 'Low',
            'due_date': date.today(),
            'assigned_to': self.user.id,
        })
        self.assertRedirects(response, reverse('task_list'))
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
    
    def test_delete_task_view(self):
        # Create a task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        # Ensure task is created
        self.assertEqual(Task.objects.count(), 1)
        
        # Delete the task
        response = self.client.post(reverse('delete_task', args=[task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 0)
