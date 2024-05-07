from re import T
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    #     ("username"),
    #     max_length=150,
    #     help_text=(
    #         "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    #     validators=[AbstractUser.username_validator],
    #     error_messages={
    #         "unique": ("Пользователь с таким email уже существует")},
    #     null=True,
    #     blank=True,
    # )

    # email = models.EmailField(('email'), unique=True,)

    # is_active = models.BooleanField(
    #     ("active"),
    #     default=False,
    #     help_text=("Designates whether this user should be treated as active. "
    #                 "Unselect this instead of deleting accounts"),
    # )

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

