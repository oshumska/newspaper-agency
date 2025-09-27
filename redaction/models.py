from django.db import models
from django.contrib.auth.models import AbstractUser


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", )


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
