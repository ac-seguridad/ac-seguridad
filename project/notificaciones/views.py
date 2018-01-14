from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .mailer import Mailer

import pdb
from ac_seguridad.models import *
from project.celery import app
import requests
import json

# Create your views here.
def index(request):
    pdb.set_trace()
    context = {}
    template = loader.get_template('ac_seguridad/index.html')
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def enviar_correo_entrada(request):
    """
        Campos:
              rif: rif del centro comercial
              nombre_estacionamiento: nombre del centro comercial
              monto_tarifa: trarifa del estacionamiento
              tipo_tarifa: "tarifa plana " if estacionamiento.tarifa_plana else "tafifa por horas"

              ticket: ticket asignado al momento de la entrada
              hora_entrada: hora de entrada del vehiculo
              <!-- hora_salida: Hora de egreso vehicular -->

              placa: carro en gestión
              email: email del dueno del carro a contactar
              nombre_dueno: dueno del vehiculo.
              apellido_dueno: Apellido del dueno del vehiculo

    """
    data_response = dict()
    if request.method == 'POST':
        data_recibida = request.POST
#         contenido = "Estimado usuario {usuario}:\n\n\n \
#         Se ha registrado un ingreso en el estacionamiento {estacionamiento} de su vehículo {placa} \
# le hemos asigando el número {ticket} \n \
#         Le recodamos: \n\
#         El estacionamiento {estacionamiento} actualmente cuenta con una tarifa {tipo_tarifa} con el monto:{monto_tarifa}. \
# Adicionalmente le recordamos que por la seguridad de su vehículo se ha asociado a su \
# número de ticket a la placa de su carro, por lo que solo con su número de \
# ticket podrá ser extraido su vehículo.\n\n \
#         Gracias por usar nuestro servicio de seguridad: AC Seguridad. \n\
#         Si no reconoce esta entrada responder a este correo.".format(
#             usuario=data_recibida['nombre_dueno'] + " " + data_recibida['apellido_dueno'],
#             estacionamiento= data_recibida['nombre_estacionamiento'],
#             placa = data_recibida['placa'],
#             monto_tarifa = data_recibida['monto_tarifa'],
#             tipo_tarifa = data_recibida['tipo_tarifa'],
#             ticket = data_recibida['ticket'],
#
#         )
#         email = EmailMessage(subject='Entrada en estacionamiento',
#                              body=contenido,
#                              to=[data_recibida['email']])
#         # email = EmailMessage('Test', 'Test', to=['anaberincon9@gmail.com'])
#         email.send()
        # pdb.set_trace()
        # mail = Mailer()
        __send_in_mail.delay(data_recibida)
        # mail.send_messages(subject='Entrada de estacionamiento',
        #            template='notificaciones/email-entrada.html',
        #            context={'usuario': data_recibida['nombre_dueno'] + " " + data_recibida['apellido_dueno'],
        #                     'estacionamiento': data_recibida['nombre_estacionamiento'],
        #                     'placa': data_recibida['placa'],
        #                     'monto_tarifa': data_recibida['monto_tarifa'],
        #                     'tipo_tarifa': data_recibida['tipo_tarifa'],
        #                     'ticket': data_recibida['ticket']
        #                     },
        #            to_emails=[data_recibida['email']])
        data_response['success'] = True

    else:
        data_response['success'] = False

    return JsonResponse(data_response)

@csrf_exempt
def enviar_correo_salida(request):
    """
        Campos:
              rif: rif del centro comercial
              nombre_estacionamiento: nombre del centro comercial

              ticket: ticket asignado al momento de la entrada

              placa: carro en gestión
              email: email del dueno del carro a contactar
              nombre_dueno: dueno del vehiculo.
              apellido_dueno: Apellido del dueno del vehiculo

    """
    data_response = dict()
    if request.method == 'POST':
        data_recibida = request.POST
#         contenido = "Estimado usuario {usuario}:\n\n\n \
#         Se ha registrado un egreso en el estacionamiento {estacionamiento} de su vehículo {placa} \
# con el número {ticket} \n \
#         Gracias por usar nuestro servicio de seguridad: AC Seguridad. \n\
#         Si no reconoce este egreso responder a este correo.".format(
#             usuario=data_recibida['nombre_dueno'] + " " + data_recibida['apellido_dueno'],
#             estacionamiento= data_recibida['nombre_estacionamiento'],
#             placa = data_recibida['placa'],
#             ticket = data_recibida['ticket'],
#
#         )
#         email = EmailMessage(subject='Entrada en estacionamiento',
#                              body=contenido,
#                              to=[data_recibida['email']])
#         # email = EmailMessage('Test', 'Test', to=['anaberincon9@gmail.com'])
#         email.send()
        __send_out_mail.delay(data_recibida=data_recibida)
        # mail = Mailer()
        # mail.send_messages(subject='Salida de estacionamiento',
        #            template='notificaciones/email-salida.html',
        #            context={'usuario': data_recibida['nombre_dueno'] + " " + data_recibida['apellido_dueno'],
        #                     'estacionamiento': data_recibida['nombre_estacionamiento'],
        #                     'placa': data_recibida['placa'],
        #                     'ticket': data_recibida['ticket']
        #                     },
        #            to_emails=[data_recibida['email']])


        data_response['success'] = True

    else:
        data_response['success'] = False
    return JsonResponse(data_response)

@app.task
def __send_in_mail(data_recibida):
    mail = Mailer()
    mail.send_messages(subject='Entrada de estacionamiento',
               template='notificaciones/email-entrada.html',
               context={'usuario': data_recibida['nombre_dueno'] + " " + data_recibida['apellido_dueno'],
                        'estacionamiento': data_recibida['nombre_estacionamiento'],
                        'placa': data_recibida['placa'],
                        'monto_tarifa': data_recibida['monto_tarifa'],
                        'tipo_tarifa': data_recibida['tipo_tarifa'],
                        'ticket': data_recibida['ticket']
                        },
               to_emails=[data_recibida['email']])

@app.task
def __send_out_mail(data_recibida):
    mail = Mailer()
    mail.send_messages(subject='Salida de estacionamiento',
               template='notificaciones/email-salida.html',
               context={'usuario': data_recibida['nombre_dueno'] + " " + data_recibida['apellido_dueno'],
                        'estacionamiento': data_recibida['nombre_estacionamiento'],
                        'placa': data_recibida['placa'],
                        'ticket': data_recibida['ticket']
                        },
               to_emails=[data_recibida['email']])
