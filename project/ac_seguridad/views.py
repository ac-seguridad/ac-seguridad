from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

import pdb
from .models import Persona
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

def afiliados(request):
    context = {}
    template = loader.get_template('ac_seguridad/afiliados.html')
    return HttpResponse(template.render(context, request))
    
def signup(request):
    context=dict()
    
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        persona_form = ac_forms.SignUpPersonaForm(request.POST)
        if (user_form.is_valid() and persona_form.is_valid()):
            # Aquí se guarda el usuario creado en AUTH users
            usuario_user = user_form.save() 
            usuario_user.refresh_from_db()
            
            # Extraemos los datos del form de persona.
            cedula_persona = persona_form.cleaned_data.get('cedula')
            email_persona = persona_form.cleaned_data.get('email')
            nombre_persona = persona_form.cleaned_data.get('nombre')
            apellido_persona = persona_form.cleaned_data.get('apellido')
            telefono_persona = persona_form.cleaned_data.get('telefono')
            
            usuario_persona = Persona(
                                usuario=usuario_user, 
                                nombre=nombre_persona,
                                apellido=apellido_persona,
                                telefono=telefono_persona,
                                cedula=cedula_persona,
                                email=email_persona)
            
            usuario_persona.save()
            usuario_user.save()
            
            # Extraer los datos de cada form.
            nombre_usuario = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            
            usuario = authenticate(username=nombre_usuario, password=raw_password)
            login(request, usuario)
            return redirect('login')
    else:
        persona_form = ac_forms.SignUpPersonaForm()
        user_form = UserCreationForm()
        
    context['user_form'] = user_form
    context['persona_form'] = persona_form
    return render(request, 'ac_seguridad/registration/signup.html', context)