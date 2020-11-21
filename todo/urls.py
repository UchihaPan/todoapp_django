"""todowoo URL Configuration

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
from todo import views
from django.contrib.auth import views
from .views import Signup,home,completedtodos,createtodo,currenttodos,viewtodo,deletetodo,completetodo


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('create/', createtodo, name='createtodo'),
    path('current/',currenttodos, name='currenttodos'),
    path('completed/', completedtodos, name='completedtodos'),
    path('todo/<int:pk>', viewtodo, name='viewtodo'),
    path('todo/<int:pk>/complete', completetodo, name='completetodo'),
    path('todo/<int:pk>/delete', deletetodo, name='deletetodo'),
]
