from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=f'user_{uuid4().hex}', max_length=100, db_index=True)
    username = models.CharField(max_length=100, default="", unique=True)

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    USERNAME_FIELD = "username"

    @staticmethod
    def create(payload: dict):
        return User(
            first_name=payload.get('first_name', ''),
            last_name=payload.get('last_name', ''),
            email=payload.get('email', '')
        )

    @staticmethod
    def get_by_email(email: str):
        try:
            return User.objects.get(email=email)
        except (Exception, User.DoesNotExist):
            return
