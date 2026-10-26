from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned','Planifié'
        IN_PROGRESS = 'in_progress','En cours'
        COMPLETED = 'completed','Terminé'
        CANCELLED = 'cancelled','Annulé'

    title = models.CharField(max_length=100)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='managed_projects') #empêche de supprimer un utilisateur tant qu'il est responsable de projets
    status = models.CharField(max_length=25,choices=Status.choices,default=Status.PLANNED)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='projects')
    description = models.TextField(blank=True,null=True)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Définir des règles de validation
    def clean(self):
        super().clean()

        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': 'La date de fin doit être postérieure ou égale à la date de début.'
                })