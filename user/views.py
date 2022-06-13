from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import (login, authenticate, logout)
from django.contrib.auth.decorators import login_required
from user.models import (Feedback, IssueReport)


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


@login_required
def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        return redirect('login')
    return redirect('homepage')


def unavailable(request):
    context = dict()
    context['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'user/unavailable.html', context=context)


def feedback(request):
    context = {}
    context['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
    if request.method == "GET":
        return render(request, 'user/feedback.html', context=context)
    else:
        name = request.POST.get('name', 'BlankName')
        feedback = request.POST.get('feedback', 'Blank message')
        message = Feedback.objects.create(name=name, message=feedback)
        message.save()
        context['response'] = "Feedback Receieved"
        return render(request, 'user/message_response.html', context=context)


def report_issue(request):
    context = {}
    context['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
    if request.method == "GET":
        return render(request, 'user/report_issue.html', context=context)
    else:
        report_kwargs = {}
        report_kwargs['name'] = request.POST.get('name', 'BlankName')
        email = request.POST.get('email', False)
        if email:
            report_kwargs['email'] = email
        report_kwargs['message'] = request.POST.get('issue_text', 'Blank message')
        issue = IssueReport.objects.create(**report_kwargs)
        issue.save()
        context['response'] = "Issue Submitted"
        return render(request, 'user/message_response.html', context=context)

def about(request):
    pass