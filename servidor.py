# !/usr/bin/env python3

import socket
from random import randint
import threading
import time
import os
import random
import json

host="192.168.1.64"
port=65432
numConn=3
buffer_size = 1024
personaje=""
personajeC=""
################################################################
#Nombres de los personajes en ingles para que sea facil reconocerlos
personajes=['batman', 'superman', 'wonder woman', 'flash', 'green lantern', 'lex luthor', 'catwoman', 'joker', 'harley quinn', 'poison ivy']
#Caracteristicas de cada personaje
personajesC= [ # Arreglo bidimiensional
    ["heroe","rico","capa","negro","sabe pelear","hombre","cabello","cabello corto","inteligente","batman"],
    ["heroe","vuela","super fuerza","visión laser","hombre","capa","cabello","cabello corto","veloz","superman"],
    ["heroe","vuela","mujer","cabello","cabello largo","super fuerza","lazo","wonder womam"],
    ["heroe","veloz","hombre","rojo","agil","cabello","cabello corto","flash"],
    ["heroe","super fuerte","verde","vuela","hombre","cabello","cabello corto","green lantern"],
    ["villano","rico","hombre","inteligente","calvo","lex luthor"],
    ["villano","mujer","negro","sabe pelear","cabello","agil","cabello corto","catwoman"],
    ["villano","hombre","inteligente","payaso","cabello","joker"],
    ["villano","mujer","cabello","cabello largo","sabe pelear","payaso","agil","harley quinn"],
    ["villano","mujer","cabello","cabello largo","agil","verde","poison ivy"]
]

#VERIFICAR QUE LA CADENA DICHA POR EL USUARIO SEA VALIDA
"""
for i in Caracteristicas de personaje elegido:  
    cont=0
    if(Cadena que manda el usuario.find(i)!=-1): #Si es diferente de -1, signifca que es correcta
        return "Si"
        break;
    cont+=1
    elif cont==len(caracteristicas): si ya recorrió todas las característica y no la encontro,regresa un NO de respuesta
        return "No"
        break
"""
#######################################################################
global NumPlayers #Es una variable global que servira de referencia a todos los clientes que se generarán
NumPlayers = 0
eleccion = randint(0, len(personajes) - 1)

personaje = personajes[eleccion]

personajeC = personajesC[eleccion]

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
        #Cuando estan todos los jugadores, se elige un personaje al azar junto con sus caracteristicas
        print("\nElegi al personaje {} con caracteristicas({})\n".format(personaje,personajeC))
        while True: #Bucle infinito, se   recorre la lista de semaforos infinitamente
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
    print("\nhilos activos:{}\n".format(threading.active_count()))
    #print("enum", threading.enumerate())
    #print("conexiones: ", len(listaconexiones))
    #print(listaconexiones)

def validarPregunta(cadena,listaConexiones,Client_conn):
    cadena=cadena.lower()
    cont = 0
    for i in personajeC:
        cont+=1
        if(cadena.find(i)!=-1): #Si encuentra alguna característica en la cadena del usuario, entonces la respuesta será si
            mensaje=cadena+"\tSi"
            print(mensaje)
            Client_conn.sendall(b'Si')
            """for j in listaConexiones: #Devolver la pregunta y respuesta a todos los jugadores
                if j==Client_conn:
                    j.sendall(b'Si') #Si se trata del jugador que hizo la pregunta, solo enviar la respuesta
                else:
                    j.sendall(mensaje.encode())"""

            break
        elif cont==len(personajeC): # de lo contrario será no
            mensaje = cadena + "\tNo"
            print(mensaje)
            Client_conn.sendall(b'No')
            """for j in listaConexiones:  # Devolver la pregunta y respuesta a todos los jugadores
                if j != Client_conn:
                    j.sendall(b'No')  # Si se trata del jugador que hizo la pregunta, solo enviar la respuesta
                else:
                    j.sendall(mensaje.encode())"""
            break


def recibir_datos_host(Client_conn, Client_addr, listaConexiones,cond,semaforo,listaSemaforos,condSem):
    #Codigo del jugador host
    global NumPlayers
    PlayerPoints = 0
    try:
        cur_thread = threading.current_thread()
        #print("Recibiendo datos del cliente {} en el {}\n".format(Client_addr, cur_thread.name))
        
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
            validarPregunta(data.decode(), listaConexiones, Client_conn)

            if not data:
                break

            #print(data.decode())
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
            validarPregunta(data.decode(), listaConexiones, Client_conn)

            if not data:
                break
            #print(data.decode())
            
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
