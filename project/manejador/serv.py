'''
ref: https://docs.python.org/3/library/socketserver.html#module-socketserver

'''

import socketserver
import sys
import os
import threading
import socket

if __name__ == "__main__":
    import servers
else:
    import manejador.servers as servers

print("host: {}, addr: {}".format(socket.gethostname(), socket.getaddrinfo(socket.gethostname(), 8081)))
HOST, PORT = '192.168.0.112', 8081
chosen_server = sys.argv[1]
server_classes = {'files':socketserver.TCPServer,
                  'forks':servers.ForkedTCPServer,
                  'hilos':servers.ThreadedTCPServer,
                 }
server_handlers= {'files':servers.FilesTCPHandler,
                  'forks':servers.ForkedTCPRequestHandler,
                  'hilos':servers.ThreadedTCPRequestHandler
                 }

# Create the server, binding to localhost on port 9999
# with server_classes[chosen_server]((HOST, PORT), server_handlers[chosen_server]) as server:
#     print("Servidor creado\n\tIP: {}\n\tPuerto: {}\n\tTipo: {}".format(HOST, PORT, chosen_server))
#     server.serve_forever()
server = server_classes[chosen_server]((HOST, PORT), server_handlers[chosen_server])
print("Servidor creado\n\tIP: {}\n\tPuerto: {}\n\tTipo: {}".format(HOST, PORT, chosen_server))
server.serve_forever()
