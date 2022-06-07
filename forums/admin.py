from django.contrib import admin
from forums.models import (ForumTopic, Post)
# Register your models here.

admin.site.register(ForumTopic)
admin.site.register(Post)