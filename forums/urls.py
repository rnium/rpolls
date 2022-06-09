from django.urls import path
from forums import views

app_name = 'forums'

urlpatterns = [
    path('', views.forums_all, name="forum_all"),
    path('create/', views.forum_create, name="forum_create"),
    path('<int:pk>/', views.forumdetail, name="forum_detail"),
    path('<int:pk>/reply/', views.reply_to_forum, name="forum_reply"),
]
