from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='myapp_user_set',  # Change related_name to avoid clash
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='myapp_user_set',  # Change related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/')

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/')
