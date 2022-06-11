from django.urls import path
from polls import views

app_name = 'polls'

urlpatterns = [
    path('', views.pollshomepage, name='index'),
    path('browse/', views.polls_all, name='browse'),
    path('<int:pk>/', views.polldetail , name='polldetails'),
    path('<int:pk>/edit', views.update_poll , name='edit_poll'),
    path('<int:pk>/vote/', views.vote_now , name='vote'),
    path('create/', views.create_poll , name='create_poll'),
    path('vote/history', views.votes_history , name='votes_history'),
]