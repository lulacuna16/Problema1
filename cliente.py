#!/usr/bin/env python3

import socket
from random import shuffle
import time
import os
import sys
import json

HOST = "192.168.1.64"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Bienvenido a Memoria")
    
    TCPClientSocket.sendall(b" ")
    data = TCPClientSocket.recv(buffer_size)    
    
    if(data.decode() == "JH"): #Código para jugador host
        numPlay = input("Ingrese el número de jugadores: \n")
        TCPClientSocket.sendall(numPlay.encode())
        data = TCPClientSocket.recv(buffer_size)    #Manda al servidor el número de jugadores
        
        TCPClientSocket.sendall(b" ")
        print("Esperando a otros jugadores...")
        data = TCPClientSocket.recv(buffer_size)    #Espera a que el servidor mande algo para que sepa que ya se ha cumplido la barrera
        TCPClientSocket.sendall(b" ")
    
    if(data.decode() == "ETC"): #Código para otros jugadores
        print("Esperando a otros jugadores...")
        TCPClientSocket.sendall(b" ")
        data = TCPClientSocket.recv(buffer_size)
        TCPClientSocket.sendall(b" ")   #Prácticamente solo sincroniza los enviar y recibir, si no luego hace cosas raras xD
        
        time.sleep(1)
    
    while True:
        print("Espere su turno: ")
        data = TCPClientSocket.recv(buffer_size)
        coord=input("Ingrese un mensaje para enviar al servidor ")
        TCPClientSocket.sendall(coord.encode())
