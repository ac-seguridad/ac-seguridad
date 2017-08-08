from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import pdb
from .models import Persona, Estacionamiento, Vehiculo
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
    
def registro_persona(request):
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
            # Authenticate regresa un objeto Usuario si logra autenticar, 
            # Retorna None si NO pudo autenticar. En este caso, como estamos 
            # creando el usuario, siempre debería autenticar.
            if usuario is not None:
                login(request, usuario)
                return redirect('area_personal')
            else:
                return redirect('login')
                
    else:
        persona_form = ac_forms.SignUpPersonaForm()
        user_form = UserCreationForm()
        
    context['user_form'] = user_form
    context['persona_form'] = persona_form
    return render(request, 'ac_seguridad/registration/signup_persona.html', context)
    
def registro_estacionamiento(request):
    context=dict()
    
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        estacionamiento_form = ac_forms.SignUpEstacionamientoForm(request.POST)
        if (user_form.is_valid() and estacionamiento_form.is_valid()):
            # Aquí se guarda el usuario creado en AUTH users
            usuario_user = user_form.save() 
            usuario_user.refresh_from_db()
            
            # Extraemos los datos del form de estacionamiento.
            rif_estacionamiento = estacionamiento_form.cleaned_data.get('rif')
            email_estacionamiento = estacionamiento_form.cleaned_data.get('email')
            nombre_estacionamiento = estacionamiento_form.cleaned_data.get('nombre')
            numero_de_puestos_estacionamiento = estacionamiento_form.cleaned_data.get('numero_de_puestos')
            acceso_restringido_estacionamiento = estacionamiento_form.cleaned_data.get('acceso_restringido')
            
            
            usuario_estacionamiento = Estacionamiento(
                                        usuario = usuario_user,
                                        rif = rif_estacionamiento,
                                        nombre = nombre_estacionamiento,
                                        numero_de_puestos = numero_de_puestos_estacionamiento,
                                        acceso_restringido = acceso_restringido_estacionamiento,
                                        email = email_estacionamiento)
            
            usuario_estacionamiento.save()
            usuario_user.save()
            
            # Extraer los datos de cada form.
            nombre_usuario = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            
            usuario = authenticate(username=nombre_usuario, password=raw_password)
            if usuario is not None:
                login(request, usuario)
                return redirect('area_personal')
            else:
                return redirect('login')
    else:
        estacionamiento_form = ac_forms.SignUpEstacionamientoForm()
        user_form = UserCreationForm()
        
    context['user_form'] = user_form
    context['estacionamiento_form'] = estacionamiento_form
    return render(request, 'ac_seguridad/registration/signup_estacionamiento.html', context)
    
@login_required
def area_personal(request):
    # Esta página sólo es visible para el usuario que ha hecho login. 
    # Django nos garantiza al usar el @login_required que sólo se podrá entrar
    # en esta página si el usuario está logueado. También, en request.user
    # estará la instancia de usuario 'User'.
    context = dict()
    usuario = request.user.persona
    
    # Obtener la lista de vehículos que la persona posee.
    query_vehiculos_usuario = Vehiculo.objects.filter(dueno=usuario.cedula)
    
    context['vehiculos_usuario'] = query_vehiculos_usuario
    context['usuario'] = usuario
    template = loader.get_template('ac_seguridad/area_personal/area_personal.html')
    return HttpResponse(template.render(context,request))
    
@login_required
def registro_vehiculo(request):
    usuario = request.user.persona
    
    context = dict()
    if request.method == 'POST':
        vehiculo_form = ac_forms.VehiculoForm(request.POST)
        if (vehiculo_form.is_valid()):
            
            # Extraemos los datos del form de estacionamiento.
            placa = vehiculo_form.cleaned_data.get('placa')
            marca = vehiculo_form.cleaned_data.get('marca')
            modelo = vehiculo_form.cleaned_data.get('modelo')
            year = vehiculo_form.cleaned_data.get('year')
            
            vehiculo = Vehiculo(
                                dueno = usuario,
                                placa = placa,
                                marca = marca,
                                modelo = modelo,
                                year = year)
            vehiculo.save()
            
            # Redirigir a area personal.
            return redirect('area_personal')
    else:
        vehiculo_form = ac_forms.VehiculoForm()
        
    context['vehiculo_form'] = vehiculo_form
    return render(request, 'ac_seguridad/area_personal/registro_vehiculo.html', context)
    