from email import message
from django.db import models
from importlib_metadata import email


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"message from - {self.name}"


class IssueReport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    message = models.TextField()

    def __str__(self):
        return f"report from - {self.name}"