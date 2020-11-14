from django.db import models
import uuid


class user(models.Model):
    uid = models.UUIDField(primary_key=True, max_length=100, unique=True, default=uuid.uuid4)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
