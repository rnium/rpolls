from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError

from django.http import HttpResponse

def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = User.objects.create(username=username)
            except IntegrityError:
                return render(request, 'user/register.html', context={'error': 'username not available', 
                                                                    'prev_values': True, 
                                                                    'username': username,
                                                                    'password1': password1,
                                                                    'password2': password2})
            user.set_password(password1)
            user.save()
            return  HttpResponse('success')
        else:
            return render(request, 'user/register.html', context={'error': 'passwords mismatch', 
                                                                    'prev_values': True, 
                                                                    'username': username,
                                                                    'password1': password1,
                                                                    'password2': password2})


# def login(request):
#     if request.method == "GET":
#         return render(request, 'user/login.html')
#     elif request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')