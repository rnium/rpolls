from django.urls import path
from polls import views

app_name = 'polls'

urlpatterns = [
    path('', views.pollshomepage, name='index'),
    path('<int:pk>/', views.polldetail , name='polldetails'),
]