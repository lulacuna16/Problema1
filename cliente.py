#!/usr/bin/env python3

import socket
from random import shuffle
import time
import os
import sys
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Bienvenido a Memoria")
    
    TCPClientSocket.sendall(b" ")
    data = TCPClientSocket.recv(buffer_size)    
    
    if(data.decode() == "JH"):
        numPlay = input("Ingrese el número de jugadores: \n")
        TCPClientSocket.sendall(numPlay.encode())
        data = TCPClientSocket.recv(buffer_size)    
        
        TCPClientSocket.sendall(b" ")
        print("Esperando a otros jugadores...")
        data = TCPClientSocket.recv(buffer_size)    
        TCPClientSocket.sendall(b" ")
        
        #print("Esperando una respuesta...")
    
    #print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
    
    if(data.decode() == "ETC"):
        print("Esperando a otros jugadores...")
        TCPClientSocket.sendall(b" ")
        data = TCPClientSocket.recv(buffer_size)
        TCPClientSocket.sendall(b" ")
        
        time.sleep(1)
        #PrintBoard(level,Board)
    
    #data =TCPClientSocket.recv(buffer_size)
    
    
    while True:
        #TCPClientSocket.sendall(b" ")
        print("Espere su turno: ")
        data = TCPClientSocket.recv(buffer_size)
        #PrintBoard(level,Board)
        coord=input("Ingrese las cordenadas de las cartas que desea ver en el formato x1,y1;x2,y2 ")
        TCPClientSocket.sendall(coord.encode())
