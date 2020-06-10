# !/usr/bin/env python3

import socket
import sys
import threading
import time
import os
import random
import json

host="127.0.0.1"
port=65432
numConn=3
buffer_size = 1024

global NumPlayers
NumPlayers = 0
#######################################################

########################################################

def servirPorSiempre(socketTcp, listaconexiones):
    global NumPlayers
    condition = threading.Condition()
    condSem = threading.Condition()
    listaSemaforos=[]
    try:
        client_conn, client_addr = socketTcp.accept()
        print("Conectado a", client_addr)
        semaforoH = threading.Semaphore(0)
        listaSemaforos.append(semaforoH)
        listaconexiones.append(client_conn)
        thread_read = threading.Thread(target=recibir_datos_host, args=[client_conn, client_addr,listaconexiones,condition,semaforoH,listaSemaforos,condSem])
        thread_read.start()
        gestion_conexiones(listaConexiones)
        with condition:
            condition.wait()
        barrier = threading.Barrier(NumPlayers-1)
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            semaforoJ = threading.Semaphore(0)
            listaSemaforos.append(semaforoJ)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr,listaconexiones,barrier,condition,semaforoJ,listaSemaforos,condSem])
            thread_read.start()
            gestion_conexiones(listaConexiones)
            if(len(listaConexiones) >= NumPlayers):
                break
        print("SALIENDO DE SERVIR POR SIEMPRE")
        #COMENZAR PLANIFICACION DE TURNOS
        
        while True:
            for sem in listaSemaforos:
                sem.release()
                print("Liberando semaforo")
                with condSem:
                    print("Esperando..")
                    condSem.wait()
        
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)

def SendToAll(Data,listaConexiones):
    print("Enviar a todos")
    for conn in listaConexiones:
        conn.sendall(b"$")
        data = conn.recv(buffer_size)
        conn.sendall(Data.encode())
        data = conn.recv(buffer_size)

def PlanificarTurnos(listaSemaforos):
    print(listaSemaforos)
        
def recibir_datos_host(Client_conn, Client_addr, listaConexiones,cond,semaforo,listaSemaforos,condSem):
    global NumPlayers
    PlayerPoints = 0
    
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(Client_addr, cur_thread.name))
        
        print("Conectado a", Client_addr)        
        data = Client_conn.recv(buffer_size)
        #print ("Recibido,", data,"   de ", Client_addr)
        Client_conn.sendall(b"JH")
        data = Client_conn.recv(buffer_size)
        
        NumPlayers = int(data.decode())
        Client_conn.sendall(b" ")
        
        data = Client_conn.recv(buffer_size)         
        with cond:
            cond.notifyAll()
        
        with cond:
            print("Esperando a otros jugadores")
            cond.wait()
            
        print("Jugadores listos Continuando..")
        Client_conn.sendall(b" ")
        data = Client_conn.recv(buffer_size)

        while True:
            print("Adquiriendo Semaforo")
            semaforo.acquire()
            print("Semaforo adquirido")
            
            Client_conn.sendall(b" ")
            #print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            if not data:
                break
            print(data.decode())           
            with condSem:
                print("Continuando...")
                condSem.notifyAll()
            
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()
    
def recibir_datos(Client_conn, Client_addr, listaConexiones,barrier,cond,semaforo,listaSemaforos,condSem):
    PlayerPoints = 0
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(Client_addr, cur_thread.name))
        print("Conectado a", Client_addr)     
        
        data = Client_conn.recv(buffer_size)
        #print ("Recibido,", data,"   de ", Client_addr)
        print("El tablero ha sido creado por otro usuario")
        #ETC: Error, tablero creado
        Client_conn.sendall(b"ETC") 
        data = Client_conn.recv(buffer_size)
        
        print(threading.current_thread().name,
          'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
        worker_id = barrier.wait()
        
        with cond:
            cond.notifyAll()
            
        Client_conn.sendall(b" ") 
        data = Client_conn.recv(buffer_size)
        
        while True:
            print("Adquiriendo Semaforo j")
            semaforo.acquire()
            print("Semaforo adquirido j")
            
            Client_conn.sendall(b" ")
            #print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            if not data:
                break
            print(data.decode())
            
            with condSem:
                condSem.notifyAll()
                print("Continuando j...")
        
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()



listaConexiones = []
#host, port, numConn = sys.argv[1:4]

#if len(sys.argv) != 4:
#    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
#    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
