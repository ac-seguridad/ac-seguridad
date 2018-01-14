
#    Este archivo es el encargado de recibir la placa leída y decidir si dejar
#    pasar a un vehículo o no, dependiendo de la configuración de este. Además,
#    busca si la placa está registrada en el sistema, en caso de estarlo, busca
#    el usuario asociado al vehículo.

#    Este archivo básicamente maneja las alertas que se generan en el sistema.


# from ac_seguridad.models import *
import requests
from mysocket import MySocket
import socket
import pdb
# Constantes.
NUM_PUERTA = 5
RIF = "12345"
HOST = "localhost"
PORT = 8000
#1234 acceso restringido
#0000 acceso no restringido
#pdb.set_trace()
# Funciones
def leer_placa():
    placa = input("Placa: ")
    return placa

# Programa comienza aquí.
# ref: https://docs.python.org/3/howto/sockets.html
# Crear un socket como cliente.
print("Creando socket")
# socket_cliente = MySocket()
# socket_cliente.connect(host=HOST, port=PORT)
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
# * registrado: si el ticket es registrado, en el caso de entrada es None

print("Preparando mensaje")
mensaje = dict()
mensaje['estacionamiento'] = RIF
mensaje['ticket'] = None
mensaje['placa'] = leer_placa()
mensaje['puerta'] = NUM_PUERTA
mensaje['tipo'] = 'placa_leida_entrada'
mensaje['lectura_automatica']= True
mensaje['registrado']=None

print("Enviando mensaje: {}".format(mensaje))
# socket_cliente.sendall_json(mensaje)
# socket_cliente.mysend("Hola, este es el mensaje\0".encode(encoding="utf-8", errors="strict"))
url = "http://{}:{}/manejador/manejar_mensaje/".format(HOST,PORT)
data_mensaje = mensaje
respuesta_request = requests.post(url, data=data_mensaje)
respuesta = respuesta_request.json()
print("Mensaje enviado")

print("Recibiendo respuesta")
# respuesta = socket_cliente.receive()
#pdb.set_trace()
print("Respuesta recibida: {}".format(respuesta))

if (respuesta['tipo'] == "OK_entrada_estacionamiento"):
    print("Luz verde.")

elif (respuesta['tipo'] == "NO_entrada_estacionamiento"):
    print("Luz roja.")

elif (respuesta['tipo'] == "NO_carro_dentro"):
    print("Luz roja.")


else:
    print("Respuesta no válida")

# socket_cliente.sock.shutdown(socket.SHUT_WR)
# socket_cliente.sock.close()
