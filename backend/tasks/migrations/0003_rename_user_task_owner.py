# Generated by Django 5.2.1 on 2025-05-16 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_collaborators'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='user',
            new_name='owner',
        ),
    ]
