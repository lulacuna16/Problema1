import threading,socket
import time
host="192.168.1.64"
port=56432
listaConexiones = []
listaHilos = []
def gestionHilo(Client_conn,i):
    #se muestra el nombre del jugador que inicio
    print(threading.current_thread().name + " Conectado")
    #Se manda al jugador el numero de conexion para control de turnos
    Client_conn.sendall(i.to_bytes(2, 'big'))

def servirPorSiempre(TCPServerSocket):
    i = 0
    while True:
        Client_conn, Client_addr = TCPServerSocket.accept()
        listaConexiones.append(Client_conn) #Se agrega la conexion del jugador a la lista
        listaHilos.append(threading.Thread(target=gestionHilo,name="J"+str(i),args=[Client_conn,i,]))
        listaHilos[i].start() #El hilo que corresponde al jugador que ingreso se crea y se agrega a la lista
        i += 1
        if (len(listaHilos)==numConn): #Cuando los hilos sean iguales a la cantiddad de jugadores se inicia juego
            for i in range(len(listaConexiones)):
                listaConexiones[i].sendall((len(listaConexiones)).to_bytes(2,'big')) #Enviar los jugadores que van a participar
            print("\nComenzando juego") #Llamada a la funcion para que inicie

numConn=int(input("Numero de jugadores: "))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((host,port))
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket)