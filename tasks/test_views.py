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

# tasks/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import date

class TaskIntegrationTest(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.login(username='user1', password='password')

    def test_task_creation_integration(self):
        # Create a task through the form
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'Description of new task',
            'status': 'Pending',
            'priority': 'Medium',
            'due_date': date.today(),
            'assigned_to': self.user1.id,
        })
        # Check that the task was saved and user is redirected
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'New Task')

    def test_task_edit_integration(self):
        # Create a task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user1
        )
        
        # Edit the task
        response = self.client.post(reverse('edit_task', args=[task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'In Progress',
            'priority': 'Low',
            'due_date': date.today(),
            'assigned_to': self.user1.id,
        })
        # Check that the task is updated
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
        self.assertRedirects(response, reverse('task_list'))

    def test_task_deletion_integration(self):
        # Create a task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user1
        )
        
        # Delete the task
        response = self.client.post(reverse('delete_task', args=[task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 0)




# tasks/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import date

# tasks/tests/test_views.py
class TaskSystemTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password')
        self.client.login(username='user1', password='password')

    def test_login_and_task_list(self):
        # Ensure the user can log in and see the task list
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tasks available.')  # Updated to match the actual message


    def test_task_creation_workflow(self):
        # Test the full creation of a task
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'Description of new task',
            'status': 'Pending',
            'priority': 'Medium',
            'due_date': date.today(),
            'assigned_to': self.user.id,
        })
        self.assertRedirects(response, reverse('task_list'))
        self.assertContains(self.client.get(reverse('task_list')), 'New Task')

    def test_task_edit_workflow(self):
        # Test editing a task
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

    def test_task_deletion_workflow(self):
        # Test deleting a task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='Pending',
            priority='Medium',
            due_date=date.today(),
            assigned_to=self.user
        )
        
        response = self.client.post(reverse('delete_task', args=[task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 0)
