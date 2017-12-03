# Django Auth.
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^manejar_mensaje/$', views.manejar_mensaje, name='manejar_mensaje'),
]
