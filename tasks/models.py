from django.db import models
from django.contrib.auth.models import AbstractUser

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    due_date = models.DateField()
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    role_choices = [('admin', 'Admin'), ('user', 'User')]
    role = models.CharField(max_length=10, choices=role_choices, default='user')

    def __str__(self):
        return self.username

