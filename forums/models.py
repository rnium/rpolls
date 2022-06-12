from django.db import models
from django.contrib.auth.models import User


class ForumTopic(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum')
    active = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Post(models.Model):
    post_text = models.TextField()
    forum = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='forumpost')
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userpost')
    added = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return f"forum({self.forum}) post"
