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

global NumPlayers #Es una variable global que servira de referencia a todos los clientes que se generarán
NumPlayers = 0

#######################################################
'''
El algoritmo tiene 2 tipos de usuarios, como en cualquier juego normal, el que crea la partida (host)
y los invitados.

Esta versión solo recibe un mensaje del servidor y lo imprime, con el respectivo planificador de turnos
Primero inserta el numero de jugadores en el primer cliente y despues corre al otro cliente
Solo funciona con más de 2, hay que ponerle un if  xD
'''
########################################################

def servirPorSiempre(socketTcp, listaconexiones):
    global NumPlayers
    condition = threading.Condition() #Este condicional nos sirve para notificar al jugador host que la barrera ha sido cumplida y se puede proceder con el juego
    condSem = threading.Condition() #Este nos sirve para notificar al planificador de turnos que el jugador a termindao su turno y que puede proceder con el proximo
    listaSemaforos=[] #Se crea esta lista de semaforos para tener un control de cada jugador, a cada jugador se le pone un semaforo
    try:
        client_conn, client_addr = socketTcp.accept()
        print("Conectado a", client_addr)
        semaforoH = threading.Semaphore(0) #Semaforo del host
        listaSemaforos.append(semaforoH) #Se agrega el semaforo a la lista de semaforos
        listaconexiones.append(client_conn)
        thread_read = threading.Thread(target=recibir_datos_host, args=[client_conn, client_addr,listaconexiones,condition,semaforoH,listaSemaforos,condSem])
        thread_read.start() #Se inicia el hilo del jugador host para pedir el numero de jugadores
        gestion_conexiones(listaConexiones)
        with condition: 
            condition.wait() #Espera a que el host notifique que ya obtuvo el numero de jugadores 
        barrier = threading.Barrier(NumPlayers-1) #Se crea la barrera
        while True:
            client_conn, client_addr = socketTcp.accept() #Comienza a aceptar las conexiones de los demás jugadores
            print("Conectado a", client_addr)
            semaforoJ = threading.Semaphore(0) #Crea el semaforo de cado jugador
            listaSemaforos.append(semaforoJ)    #se agrega a la lista de semaforos
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr,listaconexiones,barrier,condition,semaforoJ,listaSemaforos,condSem])
            thread_read.start()
            gestion_conexiones(listaConexiones)
            if(len(listaConexiones) >= NumPlayers): #Se verifica que ya no se acepten más conexiones de otros jugadores
                break
        print("SALIENDO DE SERVIR POR SIEMPRE")
        #COMENZAR PLANIFICACION DE TURNOS
        while True: #Bucle infinito, se recorre la lista de semaforos infinitamente
            for sem in listaSemaforos:
                sem.release() #Se liberan los semaforos en la lista uno por uno, el primero es el del host
                with condSem:
                    condSem.wait() #Se espera hasta que el jugador diga notifique que acabo
        
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
  
def recibir_datos_host(Client_conn, Client_addr, listaConexiones,cond,semaforo,listaSemaforos,condSem):
    #Codigo del jugador host
    global NumPlayers
    PlayerPoints = 0
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(Client_addr, cur_thread.name))
        
        print("Conectado a", Client_addr)        
        data = Client_conn.recv(buffer_size)
        #print ("Recibido,", data,"   de ", Client_addr)
        Client_conn.sendall(b"JH") #Manda al cliente el codigo JH jugador host
        data = Client_conn.recv(buffer_size) #recibe el numero de jugadores
        
        NumPlayers = int(data.decode()) #Actualiza la variable global
        Client_conn.sendall(b" ") #Envia algo al cliente para que continue
        
        data = Client_conn.recv(buffer_size)         
        with cond:
            cond.notifyAll() #Notifica que ya obtuvo el numero de jugadores
        
        with cond:
            print("Esperando a otros jugadores")
            cond.wait() #Espera a que la barrera se haya cumplido. (Le puse la condicion en vez de la barrera xD)
            
        print("Jugadores listos Continuando..")
        Client_conn.sendall(b" ")
        data = Client_conn.recv(buffer_size)

        while True:
            semaforo.acquire() # El host adquiere el semaforo
    
            Client_conn.sendall(b" ")
            #print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size) #Recibe mensaje que envia el cliente
            if not data:
                break
            print(data.decode())           
            with condSem:
                condSem.notifyAll() #Indica al planificador de turnos que ya acabo de usar su semaforo y que continue con el proximo
            
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()
    
def recibir_datos(Client_conn, Client_addr, listaConexiones,barrier,cond,semaforo,listaSemaforos,condSem):
    #Codigo para los otros jugadores, es muy parecido xD
    PlayerPoints = 0
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(Client_addr, cur_thread.name))
        print("Conectado a", Client_addr)     
        
        data = Client_conn.recv(buffer_size)
        print("El tablero ha sido creado por otro usuario")
        #ETC: Error, tablero creado
        Client_conn.sendall(b"ETC") #Indica al cliente que sera tratado como un jugador no host
        data = Client_conn.recv(buffer_size)
        
        #Espera a que se cumpla la barrera
        print(threading.current_thread().name,
          'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
        worker_id = barrier.wait()
        
        with cond:
            cond.notifyAll() #Notifica al host que la barrera ya se ha cumplido
            
        Client_conn.sendall(b" ") 
        data = Client_conn.recv(buffer_size)
        
        while True:
            semaforo.acquire() #Adquiere su semaforo
            
            Client_conn.sendall(b" ")
            #print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size) #Recibe mensaje del cliente
            if not data:
                break
            print(data.decode())
            
            with condSem:
                condSem.notifyAll() #Notifica que su turno ha terminado
        
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()



listaConexiones = []
serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
