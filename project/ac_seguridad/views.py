from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from . import forms as ac_forms

def index(request):
    context = {}
    template = loader.get_template('ac_seguridad/index.html')
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the polls index.")
    
def ver_pagina(request):
    context = {}
    template = loader.get_template('ac_seguridad/ver_pagina.html')
    return HttpResponse(template.render(context, request))
    
def signup(request):
    if request.method == 'POST':
        form = ac_forms.SignUpForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.refresh_from_db()  # load the profile instance created by the signal
            usuario.usuario.cedula = form.cleaned_data.get('cedula')
            usuario.usuario.email = form.cleaned_data.get('email')
            usuario.usuario.nombre = form.cleaned_data.get('nombre')
            usuario.usuario.apellido = form.cleaned_data.get('apellido')
            usuario.usuario.telefono = form.cleaned_data.get('telefono')
            usuario.save()
            raw_password = form.cleaned_data.get('password1')
            usuario = authenticate(username=usuario.username, password=raw_password)
            login(request, usuario)
            return redirect('login')
    else:
        form = ac_forms.SignUpForm()
    return render(request, 'ac_seguridad/registration/signup.html', {'form': form})
    # context = dict()
    # template = loader.get_template('ac_seguridad/registration/signup.html')
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         # If user is None, then the authentication failed. However, 
    #         # as we're getting the info from the sign up form, it should
    #         # always login
    #         user = authenticate(username=username, password=raw_password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('index')
    #         else:
    #             return redirect('login')
    # else:
    #     context['form'] = UserCreationForm()
    
    # return HttpResponse(template.render(context,request))