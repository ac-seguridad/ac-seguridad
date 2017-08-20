'''
ref: https://docs.python.org/3/library/socketserver.html#module-socketserver 
 
'''

import socketserver
import servers
import sys
import threading
import socket

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    chosen_server = sys.argv[1]
    server_classes = {'files':socketserver.TCPServer,
                      'forks':servers.ForkedTCPServer,
                      'hilos':servers.ThreadedTCPServer,
                     }
    server_handlers= {'files':servers.FilesTCPHandler,
                      'forks':servers.ForkedTCPRequestHandler,
                      'hilos':servers.ThreadedTCPRequestHandler
                     }
        
    # # Create the server, binding to localhost on port 9999
    # with socketserver.TCPServer((HOST, PORT), servers.ThreadedTCPRequestHandler) as server:
    #     # Activate the server; this will keep running until you
    #     # interrupt the program with Ctrl-C
    #     server.serve_forever()
    
    # Create the server, binding to localhost on port 9999
    with server_classes[chosen_server]((HOST, PORT), server_handlers[chosen_server]) as server:
        server.serve_forever()
    