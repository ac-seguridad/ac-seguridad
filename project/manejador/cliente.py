'''
    Este archivo es el encargado de recibir la placa leída y decidir si dejar 
    pasar a un vehículo o no, dependiendo de la configuración de este. Además,
    busca si la placa está registrada en el sistema, en caso de estarlo, busca
    el usuario asociado al vehículo.
    
    Este archivo básicamente maneja las alertas que se generan en el sistema.
'''

# from ac_seguridad.models import *
from mysocket import MySocket
import socket

# Constantes.
NUM_PUERTA = 1
RIF = "J-1234"

# Funciones
def leer_placa():
    placa = input("Placa: ")
    return placa
    
# Programa comienza aquí.
# ref: https://docs.python.org/3/howto/sockets.html
# Crear un socket como cliente.
print("Creando socket")
socket_cliente = MySocket()
socket_cliente.connect(host='localhost', port=8081)
print("Socket conectado.")

# Enviar primer mensaje:
# Estructura del primer mensaje:
# * RIF: lleno
# * ticket: None.
# * placa: llena.
# * accion: entrada.
# * tipo: llena ('placa_leida')
# * puerta: llena.
print("Preparando mensaje")
mensaje = dict()
mensaje['estacionamiento'] = RIF
mensaje['ticket'] = None
mensaje['placa'] = leer_placa()
mensaje['puerta'] = NUM_PUERTA
mensaje['accion'] = 'entrada'
mensaje['tipo'] = 'placa_leida'

print("Enviando mensaje: {}".format(mensaje))
socket_cliente.sendall_json(mensaje)
# socket_cliente.mysend("Hola, este es el mensaje\0".encode(encoding="utf-8", errors="strict"))
print("Mensaje enviado")

print("Recibiendo respuesta")
respuesta = socket_cliente.receive()
print("Respuesta recibida: {}".format(respuesta))

if (respuesta['tipo'] == "OK_entrada_estacionamiento"):
    print("Luz verde.")
    
elif (respuesta['tipo'] == "NO_entrada_estacionamiento"):
    print("Luz roja.")
else:
    print("Respuesta no válida")

socket_cliente.sock.shutdown(socket.SHUT_WR)
socket_cliente.sock.close()





