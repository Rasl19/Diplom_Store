from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    SEX_CHOICES = [
        ('male', 'Муж'),
        ('female', 'Жен'),
    ]
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=True, null=True)
