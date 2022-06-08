from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import (login, authenticate, logout)

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
            login(request, user)
            return redirect('polls:index')
        else:
            return render(request, 'user/register.html', context={'error': 'passwords mismatch', 
                                                                    'prev_values': True, 
                                                                    'username': username,
                                                                    'password1': password1,
                                                                    'password2': password2})


def userlogin(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            return render(request, 'user/login.html', context={'error': 'invalid credentials'})