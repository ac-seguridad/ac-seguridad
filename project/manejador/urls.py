# Django Auth.
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='manejador'),
]