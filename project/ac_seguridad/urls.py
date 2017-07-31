# Django Auth.
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'ac_seguridad/registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'ac_seguridad/registration/logout.html'}, name='logout'),
]