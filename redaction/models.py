from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(default=datetime.now)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="topics_newspapers"
    )
    sub_topic = models.ManyToManyField(
        Topic,
        blank=True,
        related_name="subtopics_newspapers",
    )
    publishers = models.ManyToManyField(get_user_model(), related_name="newspapers")

    def __str__(self):
        return f"{self.topic.name}: {self.title}"

    class Meta:
        ordering = ("published_date",)
