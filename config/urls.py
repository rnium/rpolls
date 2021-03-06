"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from user.views import (register, userlogin, userlogout, unavailable, feedback, report_issue, handler404)
from polls.views import homepageview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepageview, name="homepage"),
    path('polls/', include('polls.urls')),
    path('forums/', include('forums.urls')),
    path('register/', register, name='register'),
    path('login/', userlogin, name='login'),
    path('logout/', userlogout, name='logout'),
    path('sourcecode/', unavailable, name='sourcecode'),
    path('rules/', unavailable, name='rules'),
    path('issue/', report_issue, name='issue'),
    path('feedback/', feedback, name='feedback'),
    path('about/', unavailable, name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'user.views.handler404'