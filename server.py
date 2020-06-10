from random import randint
from time import time
import socket,threading,logging
from threading import Lock

def servirPorSiempre(TCPServerSocket):
    global listaConexiones
    i=0
    #try:
    while True:
        Client_conn, Client_addr = TCPServerSocket.accept()
        listaConexiones.append(Client_conn)
        numJ=Client_conn.recv(int(buffer_size / 2))
        numJ=int.from_bytes(numJ,'big')
        if numJ==1:
            print("Comienza")
        else:
            print("Conectado a: {}".format(Client_addr))

HOST = "192.168.1.64"  # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024
listaConexiones=[]
lock=threading.Lock()

#b=threading.Barrier(numConn)
cont=0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")
    servirPorSiempre(TCPServerSocket)
