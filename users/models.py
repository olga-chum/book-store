from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

