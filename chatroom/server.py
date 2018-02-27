# Server side of chat room. 
import socket
import select
import sys
from thread import *

# Some initial setup 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Prompt user running the program to start the server. Could be 
# hardcoded or included as a command line argument as well.
ip_address = str(raw_input("What is the IP address?"))
port = int(raw_input("What is the port number?"))
server.bind((ip_address, port))
 

# Set the number of clients allowed.
number_of_clients = 20
server.listen(number_of_clients)
clients = []
 

def client_thread(connection, address):
    """
    Starts the client thread as client programs try to access the server.
    
    connection : The connection instance associated with the client.
    address : The address instance associated with the client.
    """
    connection.send("Chatroom instantiated.")
 
    # Continue indefinitely.
    while True:
            try:
                message = connection.recv(2048)
                if message:
 
                    broadcast_message = address[0] + " : " + message
                    print(broadcast_message)
                    broadcast(broadcast_message, connection)
                else:
                    remove(connection)
            except:
                continue

def broadcast(message, connection):
    """
    Sends each client the message sent and remove any invalid connections.
    
    message : The message to be broadcast.
    connection : The specific instance.
    """
    for client in clients:
        if client!=connection:
            try:
                client.send(message)
            except:
                client.close()
                if connection in list_of_clients:
                    clients.remove(connection)
 
# kick off client threads for each connection
while True:
    """
    Start up the server until the session is cancelled.
    """
    connection, address = server.accept()
    clients.append(connection)
    print address[0] + " has been connected"
 
    start_new_thread(client_thread,(connection,address))    
 
connection.close()
server.close()
