"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.shortcuts import HttpResponse, redirect, render
from . import views, search, kg_admin, feedback




def singer_query(request):
    return render(request, 'graph.html')


def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('graph/', singer_query),
    path('search/', search.query),
    # path('kg_admin/', kg_admin),
    path('feedback/', feedback.feedback),
    path('sendfeedback/', feedback.sendfeedback),
    path('kg_admin/', kg_admin.admin),    path('kg_admin/feedback/', kg_admin.feedback),
    path('kg_admin/singer/', kg_admin.singer),
    path('kg_admin/company/', kg_admin.company),
    path('kg_admin/school/', kg_admin.school),
    path('kg_admin/add_singer/',kg_admin.add_singer)
]
