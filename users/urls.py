'''Defines URL Patterns for Users'''
from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    #Login Page
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name = 'login'),
    #log out user and return to homepage
    url(r'^logout/$', views.logout_view, name = 'logout'),
    #Page to resgister new user
    url(r'^register/$', views.register, name = 'register'),
]