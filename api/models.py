from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Обычный пользователь'),
    ]

    confirmation_code = models.UUIDField(
        blank=True,
        editable=False,
        null=True,
        unique=True
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    bio = models.TextField()

    @property
    def is_moderator(self):
        return self.role == 'moderator'
