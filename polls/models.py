from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    title = models.CharField(max_length=250)
    banner = models.ImageField(upload_to='polls/images/', default='polls/images/default.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll')
    public = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Choice(models.Model):
    choicetext = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choice')

    def __str__(self):
        return self.choicetext


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choicevote')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='pollvote')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uservote')
    vote_time = models.DateTimeField(auto_now_add=True)
    vote_update_time = models.DateTimeField(auto_now=True)

