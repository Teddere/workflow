from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', "Administrateur"
        MANAGER = 'manager', 'Manager'
        MEMBER = 'member', 'Membre'

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    bio = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.username
