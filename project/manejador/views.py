from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import pdb
from ac_seguridad.models import *
from project.celery import app
import requests

# Create your views here.
def index(request):
    context = {}
    template = loader.get_template('ac_seguridad/index.html')
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the polls index.")

HOST = "localhost"
PORT = 8000
@csrf_exempt
def manejar_mensaje(request):
    '''
        args:
            mensaje: es un diccionario que contiene las claves definidas en keys.
        keys:
            estacionamiento: es el rif del estacionamiento, con formato J-XXXXXXXX.
            placa: refiere a la placa del vehículo con formato venezolano.
            puerta: refiere a la puerta de entrada del estacionamiento.
            tipo: tipo de mensaje y sus valores están dentro de tipos.
            ticket:
            accion: entrada o salida.
        tipos:

            entrada:
                entrada_estacionamiento,
            salida:
                salida_estacionamiento
                NO_ticket_no_encontrado
        returns: devuelve al cliente un mensaje diciendo 'OK_entrada' o 'NO_entrada'
    '''
    mensaje = request.POST
    tipo = mensaje['tipo']
    rif = mensaje['estacionamiento']
    placa = mensaje['placa']
    puerta = mensaje['puerta']
    lectura_automatica = mensaje['lectura_automatica']

    respuesta = mensaje.copy()
    vehiculo = None
    estacionamiento = Estacionamiento.objects.get(rif=rif)
    respuesta['lectura_automatica']= None
    respuesta['registrado']= None

    #Validar_existencia: Falso no se encuentra, True: se encuentra.
    dentro= validar_existencia(placa)
    print( "Está el carro dentro: {}".format(dentro) )
    # Entrada al estacionamiento

    if(dentro == False):

        if (tipo == 'placa_leida_entrada'):
            # Como nos aseguramos que SIEMPRE vamos a recibir una placa válida,
            # no tenemos que hacer esas verificaciones.
            try:
                vehiculo = Vehiculo.objects.get(placa=placa)

            except Vehiculo.DoesNotExist:
                # TODO: ver si el estacionamiento permite entrada o no.
                print("el Vehiculo {} no existe en la base de datos".format(placa))

            #vehiculo registrado
            if (vehiculo is not None):
                respuesta['tipo'] = "OK_entrada_estacionamiento"
                ticket = generar_ticket_registrados(vehiculo,estacionamiento)
                respuesta['ticket'] = ticket.numero_ticket
                generar_actividad(estacionamiento=estacionamiento,
                                  ticket=ticket,
                                  vehiculo=vehiculo,
                                  persona = vehiculo.dueno,
                                  tipo= respuesta['tipo']

                                  )
                if (vehiculo.dueno.enviar_correo):
                    enviar_mensaje_entrada(estacionamiento=estacionamiento,
                                   ticket=ticket,
                                   vehiculo=vehiculo,
                                   persona=vehiculo.dueno,
                                   )
                if(mensaje['lectura_automatica'] == True):
                    generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='entrada_exitosa', usuario= vehiculo.dueno.cedula)
                else:
                    generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='entrada_manual', usuario= vehiculo.dueno.cedula)

            #genera un ticket de los no registrados pero si hay acceso
            if ((vehiculo is None) and (not estacionamiento.acceso_restringido)):
                respuesta['tipo'] = "OK_entrada_estacionamiento"
                respuesta['ticket'] = generar_ticket_no_registrados(placa,estacionamiento)
                if(mensaje['lectura_automatica'] == True):
                    generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='entrada_exitosa', usuario= None)
                else:
                    generar_alerta(rif=estacionamiento, placa=placa ,tipo_alerta='entrada_manual', usuario= None)

            #No permite entrada por no estar registrado y tener acceso rest.
            if ((vehiculo is None) and (estacionamiento.acceso_restringido)):
                respuesta['tipo'] = "NO_entrada_estacionamiento"
                respuesta['ticket'] = None
                #aqui podria generarse una alerta de denegación de entrada.




    else:
        #Salida de vehiculo
        if ( tipo=='placa_leida_salida'):
            registrado = mensaje["registrado"]
            ticket = mensaje["ticket"]
            if (not registrado):
                try:
                #Lo primero que se hace es listar por No resgistrado
                #para evitar el caso en que el carro se registre estando dentro
                    ticket=TicketNoRegistrado.objects.get(numero_ticket=ticket)
                    if (ticket.pagado):
                        if (ticket.placa== mensaje["placa"]):
                            ticket.hora_salida = timezone.now()
                            ticket.save()
                            respuesta['tipo']= "OK_salida_estacionamiento"
                            generar_alerta(rif=estacionamiento, placa = placa, tipo_alerta = 'salida_exitosa', usuario = None)

                        else:
                            respuesta['tipo']="NO_ticket_placa"
                            generar_alerta(rif= estacionamiento,placa=placa,tipo_alerta='no_coincidencia', usuario= None)
                    else:
                        respuesta['tipo']= "NO_ticket_pagado"
                except:
                    respuesta['tipo']= "NO_ticket_no_encontrado"
            else:
                try:
                    # Verificamos si el ticket exite.
                    ticket=Ticket.objects.get(numero_ticket=ticket)
                    if (ticket.pagado):
                        if (ticket.placa.placa == mensaje["placa"]):
                            ticket.hora_salida = timezone.now()
                            ticket.save()
                            respuesta['tipo']= "OK_salida_estacionamiento"
                            if(mensaje['lectura_automatica'] == True):
                                generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='salida_exitosa', usuario= None)
                            else:
                                generar_alerta(rif=estacionamiento, placa=placa ,tipo_alerta='salida_manual', usuario= None)
                            if (ticket.vehiculo.dueno.enviar_correo):
                                enviar_mensaje_salida(estacionamiento=estacionamiento,
                                               ticket=ticket,
                                               vehiculo=ticket.vehiculo,
                                               persona=ticket.vehiculo.dueno,
                                               )
                            # generar_actividad(estacionamiento=estacionamiento,
                            #                   ticket=ticket,
                            #                   vehiculo= vehiculo,
                            #                   persona = vehiculo.dueno,
                            #                   tipo= respuesta['tipo'])
                        else:
                            respuesta['tipo']="NO_ticket_placa"
                            if(mensaje['lectura_automatica'] == True):
                                generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='NO_ticket_placa_exitoso', usuario= None)
                            else:
                                generar_alerta(rif=estacionamiento, placa=placa ,tipo_alerta='NO_ticket_placa_manual', usuario= None)
                            # generar_actividad (estacionamiento=estacionamiento,
                            #                    ticket=ticket,
                            #                    vehiculo=vehiculo,
                            #                    persona = vehiculo.dueno,
                            #                    tipo= respuesta['tipo']
                            #                     )
                    else:
                        respuesta['tipo']= "NO_ticket_pagado"
                        if(mensaje['lectura_automatica'] == True):
                            generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='NO_ticket_pagado_exitoso', usuario= None)
                        else:
                            generar_alerta(rif=estacionamiento, placa=placa ,tipo_alerta='NO_ticket_pagado_manual', usuario= None)

                except:
                    print("Ticket No encontrado")
                    respuesta['tipo']= "NO_ticket_no_encontrado"
                    if(mensaje['lectura_automatica'] == True):
                        generar_alerta(rif=estacionamiento, placa=placa, tipo_alerta='NO_ticket_no_encontrado_exitoso', usuario= None)
                    else:
                        generar_alerta(rif=estacionamiento, placa=placa ,tipo_alerta='NO_ticket_no_encontrado_manual', usuario= None)
        else:
            respuesta['tipo']= "NO_carro_dentro"
            generar_alerta(rif= estacionamiento,placa=placa,tipo_alerta='carro_dentro',usuario= None)
    return JsonResponse(respuesta)

def generar_ticket_registrados(vehiculo,estacionamiento):
    ticket = Ticket(placa =  vehiculo,
                    rif = estacionamiento,
                    hora_entrada =  timezone.now(),
                    hora_salida =  None,
                    pagado = False
                   )
    ticket.save()
    return ticket

def generar_ticket_no_registrados(placa,estacionamiento):
    ticket = TicketNoRegistrado(placa =  placa,
                    rif = estacionamiento,
                    hora_entrada =  timezone.now(),
                    hora_salida =  None,
                    pagado = False
                   )
    ticket.save()
    return ticket.numero_ticket

def generar_alerta(usuario, placa, rif,tipo_alerta):
    """Tipos de alerta:
    jj
    """
    alerta = Alerta(vehiculo = placa,
                    usuario = usuario,
                    estacionamiento =rif,
                    tipo = tipo_alerta,
                    )
    alerta.save()


def generar_actividad(estacionamiento, vehiculo, persona, tipo, ticket=None):
    actividad = Actividad(estacionamiento=estacionamiento,
                          vehiculo=vehiculo,
                          usuario=persona,
                          tipo=tipo,
                          ticket=ticket,
                          fecha=timezone.now())
    actividad.save()

# ***********************************************************************************Enviar Mensaje

# @app.task
def enviar_mensaje_entrada(estacionamiento, vehiculo, ticket, persona):
    url = "http://{}:{}/notificaciones/enviar_correo_entrada/".format(HOST,PORT)
    data_mensaje = {
        'rif': estacionamiento.rif,
        'nombre_estacionamiento': estacionamiento.nombre,
        'monto_tarifa': estacionamiento.monto_tarifa,
        'tipo_tarifa': "tarifa plana" if estacionamiento.tarifa_plana else "tarifa por horas",
        'ticket': ticket.numero_ticket,
        'placa': vehiculo,
        'email':vehiculo.dueno.email,
        'nombre_dueno': vehiculo.dueno.nombre,
        'apellido_dueno': vehiculo.dueno.apellido,
    }
    respuesta_request = requests.post(url, data=data_mensaje)
    respuesta = respuesta_request.json()

# @app.task
def enviar_mensaje_salida(estacionamiento, vehiculo, ticket, persona):

    url = "http://{}:{}/notificaciones/enviar_correo_salida/".format(HOST,PORT)
    data_mensaje = {
        'rif': estacionamiento.rif,
        'nombre_estacionamiento': estacionamiento.nombre,
        'monto_tarifa': estacionamiento.monto_tarifa,
        'tipo_tarifa': "tarifa plana" if estacionamiento.tarifa_plana else "tarifa por horas",
        'ticket': ticket.numero_ticket,
        'placa': vehiculo,
        'email':vehiculo.dueno.email,
        'nombre_dueno': vehiculo.dueno.nombre,
        'apellido_dueno': vehiculo.dueno.apellido,
    }
    respuesta_request = requests.post(url, data=data_mensaje)
    respuesta = respuesta_request.json()

#validar si un carro se encuentra dentro antes de entrar.
#false no está, true está
def validar_existencia(placa):

    aux1 = Ticket.objects.filter(placa=placa,hora_salida__isnull = True).count()
    aux2 = TicketNoRegistrado.objects.filter(placa=placa, hora_salida__isnull = True).count()
    print("aux1: {} y aux2: {}".format(aux1,aux2))

    if ( (aux1 == 0) and (aux2 == 0)):
        return False
    else:
        return True
        #return False Quita validación de carro dentro
