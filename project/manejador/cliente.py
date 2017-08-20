'''
    Este archivo es el encargado de recibir la placa leída y decidir si dejar 
    pasar a un vehículo o no, dependiendo de la configuración de este. Además,
    busca si la placa está registrada en el sistema, en caso de estarlo, busca
    el usuario asociado al vehículo.
    
    Este archivo básicamente maneja las alertas que se generan en el sistema.
'''

# from ac_seguridad.models import *
from mysocket import MySocket

rif = 'J-1234'
puerta = 1
placa = 'AE8MB'
tipo = 'Salida'
    
# Programa comienza aquí.
# ref: https://docs.python.org/3/howto/sockets.html
# Crear un socket como cliente.
print("Creando socket")
socket_cliente = MySocket()
socket_cliente.connect(host='localhost', port=9999)
print("Socket conectado.")

# Enviar mensaje:
print("Preparando mensaje")
mensaje = dict()
mensaje['estacionamiento'] = rif
mensaje['placa'] = placa
mensaje['puerta'] = puerta
mensaje['tipo'] = tipo

print("Enviando mensaje: {}".format(mensaje))
socket_cliente.sendall_json(mensaje)
# socket_cliente.mysend("Hola, este es el mensaje\0".encode(encoding="utf-8", errors="strict"))
print("Mensaje enviado")





