from time import time
import socket

#HOST = str(input("Ingrese IP del servidor: "))  # The server's hostname or IP address
#PORT = int(input("Ingrese Puerto del servidor: "))  # The port used by the server
HOST = "192.168.1.64" # Standard loopback interface address (localhost)
PORT = 56432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    numJ = int.from_bytes(TCPClientSocket.recv(buffer_size), 'big')
    print("Jugador {}".format(numJ)) #Recibe el numero de jugador que correspones
    Jugadores = int.from_bytes(TCPClientSocket.recv(buffer_size), 'big')
    print("Jugadores conectados: {}".format(Jugadores)) #Muestra todos los jugadores que van a participar
