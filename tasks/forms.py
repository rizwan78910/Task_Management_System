from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserCreateForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.role_choices, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
