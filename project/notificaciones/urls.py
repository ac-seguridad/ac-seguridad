# Django Auth.
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^enviar_correo_entrada/$', views.enviar_correo_entrada, name='enviar_correo_entrada'),
    url(r'^enviar_correo_salida/$', views.enviar_correo_entrada, name='enviar_correo_salida'),
]
