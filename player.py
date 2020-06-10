from time import time
import socket

#HOST = str(input("Ingrese IP del servidor: "))  # The server's hostname or IP address
#PORT = int(input("Ingrese Puerto del servidor: "))  # The port used by the server
HOST = "192.168.1.64" # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    numJ=int(input("Comenzar partida?\n1.Si\t2.No, esperar mas jugadores\n"))#El jugador decide si comenzar o esperar a que se conecten mas jugadores
    TCPClientSocket.sendall(numJ.to_bytes(2,'big'))