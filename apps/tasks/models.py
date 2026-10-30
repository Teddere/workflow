from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.projects.models import Project


class Task(models.Model):
    class Status(models.TextChoices):
        TODO='todo','À faire'
        IN_PROGRESS='in_progress','En cours'
        COMPLETED='completed','Terminée'
        BLOCKED='blocked','Bloquée'

    class Priority(models.TextChoices):
        HIGH='high','Haut'
        MEDIUM='medium','Moyenne'
        LOW='low','Basse'

    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True, null=True, related_name='assigned_tasks')
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=20, choices=Status.choices,default=Status.TODO)
    priority=models.CharField(max_length=20, choices=Priority.choices,default=Priority.MEDIUM)
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if self.project_id and self.due_date:
            if self.project.start_date and self.due_date < self.project.start_date:
                raise ValidationError({
                    'due_date':"L'échéance ne peut pas être antérieure à la date de début du projet."
                })
