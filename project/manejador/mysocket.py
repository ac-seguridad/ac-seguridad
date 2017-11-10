'''
    Programa que define de manera muy sencilla una clase para usar sockets.
'''
import socket
import json
import pdb

# Referencia: https://docs.python.org/3/howto/sockets.html
# Referencia: https://stackoverflow.com/questions/2751098/sending-data-as-instances-using-python-sockets
class MalformedMessage(Exception): pass
class ConnectionClosed(Exception): pass

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            # Crea por defecto un socket de IPv4 (AF_INET) y de TCP (SOCK_STREAM)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
            
        self.delimiter= '\r\n'
            
    def accept(self):
        (clientsocket, address) = self.sock.accept()
        return (MySocket(clientsocket), address)
        
    def close(self):
        self.sock.close()

    def connect(self, host, port):
        self.sock.connect((host, port))
        
    def bind(self,hostname=None,port=None):
        if hostname is None:
            hostname = socket.gethostname()
            
        if port is None:
            port = 80
            
        self.sock.bind((hostname,port))
        
    def listen(self,number_connections=None):
        if number_connections is None:
            number_connections = 5
        self.sock.listen(number_connections)

    def sendall_json(self, obj):
        data = json.dumps(obj)
        size = len(data)
        msj = "{}{}{}".format(size,self.delimiter, data).encode(encoding="utf-8", errors="strict")
        self.sock.sendall(msj)
        
    def peek(self, buflen):
        data = self.sock.recv(buflen, socket.MSG_PEEK)
        return data
        
    def read_exactly(self, buflen):
        data = ''
        while len(data) != buflen:
            data += self.sock.recv(buflen - len(data)).decode(encoding="utf-8")
            # data.append(chunk)
        return data
        
    def receive(self):
        # Vemos si hay algún mensaje en 1024 bytes de data.
        peekdata = self.peek(1024)
        if peekdata == '':
            raise ConnectionClosed
        
        # Vemos si llegó el fin de linea en los primeros 1024 bytes, y obtenemos
        # su posición en el arreglo de bytes.
        sizepos = peekdata.find(self.delimiter.encode(encoding="utf-8", errors="strict"))
        if sizepos == -1:
            raise MalformedMessage('Did not find the delimiter in message %r' % peekdata)
        
        # Ahora leemos el tamaño del mensaje
        sizedata = self.read_exactly(sizepos)
        try:
            size = int(sizedata)
        except ValueError:
            raise MalformedMessage(
                'size data %r could not be converted to an int' % sizedata)
        
        # Consumimos el delimitador.    
        self.read_exactly(len(self.delimiter))
        
        # Leemos lo que queda del mensaje.
        data = self.read_exactly(size)
        return json.loads(data)
