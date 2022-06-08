from django.urls import path
from polls.views import (pollshomepage)

urlpatterns = [
    path('', pollshomepage, name='index'),
]