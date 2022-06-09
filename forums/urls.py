from django.urls import path
from forums import views

app_name = 'forums'

urlpatterns = [
    path('', views.forums_all, name="forum_all"),
    path('<int:pk>/', views.forumdetail, name="forum_detail"),
]
