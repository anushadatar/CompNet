# Client side of chat room. 

import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = str(raw_input("What is the IP address?"))
port =  int(raw_input("What is the port number?"))

server.connect((ip_address, port))

while True:
    """
    Continue indefinitely for the connection.
    """
    sockets = [sys.stdin, server]
 
    read_sockets,write_socket, error_socket = select.select(sockets,[],[])
 
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write("You : ")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
