from django.db import models
from django.contrib.auth.models import User

# Model for Task
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
        ('archived', 'Archivado'),
        ('deleted', 'Eliminado'),
        ('canceled', 'Cancelado'),
        ('failed', 'Fallido'),
        ('on_hold', 'En espera'),
        ('skipped', 'Omitido'),
        ('paused', 'Pausado'),
        ('resumed', 'Reanudado'),
        ('rejected', 'Rechazado'),
        ('approved', 'Aprobado'), 
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    collaborators = models.ManyToManyField(User, related_name='collaborative_tasks', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title