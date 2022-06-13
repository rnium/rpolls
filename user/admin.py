from django.contrib import admin
from user.models import (Feedback, IssueReport)
# Register your models here.
admin.site.register(Feedback)
admin.site.register(IssueReport)