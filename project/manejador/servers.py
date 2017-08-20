import socketserver

import socket
import threading
import os
import socketserver
import json
import mysocket

class MalformedMessage(Exception): pass
class ConnectionClosed(Exception): pass

##############################################################################
############################## TCP y FILES ###################################
##############################################################################
class FilesTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())


##############################################################################
############################## HILOS Y TCP ###################################
##############################################################################
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # data = str(self.request.recv(1024), 'ascii')
        # cur_thread = threading.current_thread()
        # response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        # self.request.sendall(response)
        
        sock = mysocket.MySocket(self.request)
        mensaje = sock.receive()
        print("Mensaje recibido: {}".format(mensaje))
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, mensaje), 'ascii')
        self.request.sendall(response)
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


##############################################################################
############################## Forks Y TCP ###################################
##############################################################################
class ForkedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        sock = mysocket.MySocket(self.request)
        mensaje = sock.receive()
        print("Mensaje recibido: {}".format(mensaje))
        response = bytes("{}: {}".format(os.getpid(), mensaje), 'ascii')
        self.request.sendall(response)

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        client(ip, port, "Hello World 1")
        client(ip, port, "Hello World 2")
        client(ip, port, "Hello World 3")

        server.shutdown()