# Django Auth.
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ver_pagina/$', views.ver_pagina, name='ver_pagina'),
    url(r'^contacto/$', views.contacto, name='contacto'),
    url(r'^afiliados/$', views.afiliados, name='afiliados'),
    
    # Parte de personas.
    url(r'^registro-persona/$', views.registro_persona, name='registro_persona'),
    url(r'^area-personal/$', views.area_personal, name='area_personal'),
    url(r'^area-personal/registro-vehiculo/$', views.registro_vehiculo, name='registro_vehiculo'),
    
    # Parte de estacionamientos.
    url(r'^registro-estacionamiento/$', views.registro_estacionamiento, name='registro_estacionamiento'),
    url(r'^area-empresas/$', views.area_empresas, name='area_empresas'),
    url(r'^area-empresas/pago-estacionamiento/$', views.pago_estacionamiento, name='pago_estacionamiento'),
    url(r'^area-empresas/pago-estacionamiento/pagar_ticket/$', views.pagar_ticket, name='pagar_ticket'),
    url(r'^area-empresas/historial_empresas/$', views.historial_empresas, name='historial_empresas'),
    
    
    # Login.
    url(r'^login/$', auth_views.LoginView.as_view(template_name='ac_seguridad/registration/login.html',redirect_field_name='area_personal'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='ac_seguridad/registration/logout.html'), name='logout'),
    # url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]