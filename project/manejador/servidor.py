'''
    Este archivo es el encargado de recibir la placa leída y decidir si dejar 
    pasar a un vehículo o no, dependiendo de la configuración de este. Además,
    busca si la placa está registrada en el sistema, en caso de estarlo, busca
    el usuario asociado al vehículo.
    
    Este archivo básicamente maneja las alertas que se generan en el sistema.
'''

# from ac_seguridad.models import *
from mysocket import MySocket

def recibirPlaca():
    # TODO: método para recibir la placa.
    return "AE338FG" # Caso donde la placa sí existe.
    # return "PLACA" # Caso donde la placa no existe.
    # return None # Caso donde no se puede leer la placa.
    
def recibirEstacionamiento():
    # TODO: método para recibir el estacionamiento.
    return "J-1231" # Caso donde el rif del estacionamiento existe. 
    # return "NO EXISTE" # Caso donde el rif del estacionamiento no existe.
    
def inicializarServidor():
    # Programa comienza aquí.
    # ref: https://docs.python.org/3/howto/sockets.html
    # Se define el socket del servidor.
    print("Creando socket")
    socket_servidor = MySocket()
    socket_servidor.bind(hostname='localhost',port=8080)
    socket_servidor.listen(number_connections=5)
    print("Socket creado, asociado al hostname '{}', puerto '{}' y número de conexiones '{}'".format('localhost',8082,5))
    
    while True:
        # Apenas se establece una conexión, se maneja apropiadamente.
        (socket_cliente, address) = socket_servidor.accept()
        # El socket obtenido en socket_cliente establece la conexión punto a punto
        # con el estacionamiento que va a enviarnos la información. Es una instancia
        # de socket.py
        
        # Recibir e imprimir lo que obtenemos del socket.
        print("Dirección IP: {}".format(address))
        # mensaje = socket_cliente.myreceive()
        mensaje_dict = socket_cliente.receive()
        print("Mensaje: {}".format(mensaje_dict))
        
inicializarServidor()