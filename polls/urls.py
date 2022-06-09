from django.urls import path
from polls import views

app_name = 'polls'

urlpatterns = [
    path('', views.pollshomepage, name='index'),
    path('browse/', views.polls_all, name='browse'),
    path('<int:pk>/', views.polldetail , name='polldetails'),
]