
#    Este archivo es el encargado de recibir la placa leída y decidir si dejar
#    pasar a un vehículo o no, dependiendo de la configuración de este. Además,
#    busca si la placa está registrada en el sistema, en caso de estarlo, busca
#    el usuario asociado al vehículo.

#    Este archivo básicamente maneja las alertas que se generan en el sistema.


# from ac_seguridad.models import *
from mysocket import MySocket
import socket
import pdb
import sys
# Constantes.
NUM_PUERTA = 5
RIF = "1231"
HOST = "localhost"
PORT = 8081
#1234 acceso restringido
#0000 acceso no restringido
#pdb.set_trace()
# Funciones
def leer_placa():
    placa = input("Placa: ")
    return placa
def leer_ticket():
    ticket = input("ticket: ")
    resgistrado = input("registrado(True,False): ")
    return ticket, resgistrado

# Programa comienza aquí.
# ref: https://docs.python.org/3/howto/sockets.html
# Crear un socket como cliente.
print("Creando socket")
socket_cliente = MySocket()
socket_cliente.connect(host=HOST, port=PORT)
print("Socket conectado.")

# Enviar primer mensaje:
# Estructura del primer mensaje:
# * RIF: lleno
# * ticket: None.
# * placa: llena.
# * tipo: llena ('placa_leida')
# * puerta: llena.
# * lectura_automatica: llena, sus posibles valores son:
            # True: lectura realizada de forma automática
            # False: lentura realizada de forma manual
            # None: No aplica la información (ejemplo, mensajes servidor-cliente)
# * registrado: llena, true o false

print("Preparando mensaje")
mensaje = dict()
mensaje['estacionamiento'] = RIF
mensaje['ticket'], mensaje['registrado'] = leer_ticket()
mensaje['placa'] = leer_placa()
mensaje['puerta'] = NUM_PUERTA
mensaje['tipo'] = 'placa_leida_salida'
mensaje['lectura_automatica']= True




print("Enviando mensaje: {}".format(mensaje))
socket_cliente.sendall_json(mensaje)
# socket_cliente.mysend("Hola, este es el mensaje\0".encode(encoding="utf-8", errors="strict"))
print("Mensaje enviado")

print("Recibiendo respuesta")
respuesta = socket_cliente.receive()
print("Respuesta recibida: {}".format(respuesta))

if (respuesta['tipo'] == "OK_salida_estacionamiento"):
    print("Luz verde.")

elif (respuesta['tipo'] == "NO_ticket_placa"):
    print("Luz roja.")

elif (respuesta['tipo'] == "NO_ticket_pagado"):
    print("Luz roja.")

elif (respuesta['tipo'] == "NO_ticket_no_encontrado"):
    print("Luz roja.")

else:
    print("Respuesta no válida")

socket_cliente.sock.shutdown(socket.SHUT_WR)
socket_cliente.sock.close()
