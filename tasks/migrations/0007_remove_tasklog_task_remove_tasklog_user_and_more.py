# Generated by Django 5.1.6 on 2025-03-04 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_task_assigned_to_task_assigned_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasklog',
            name='task',
        ),
        migrations.RemoveField(
            model_name='tasklog',
            name='user',
        ),
        migrations.RemoveField(
            model_name='taskperformance',
            name='task',
        ),
        migrations.RemoveField(
            model_name='taskperformance',
            name='user',
        ),
        migrations.RemoveField(
            model_name='task',
            name='assigned_users',
        ),
        migrations.RemoveField(
            model_name='task',
            name='progress',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='TaskLog',
        ),
        migrations.DeleteModel(
            name='TaskPerformance',
        ),
    ]
