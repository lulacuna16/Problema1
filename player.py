#!/usr/bin/env python3


from random import shuffle
import time, logging, pyaudio, wave, socket
import os
import sys
from pathlib import Path

HOST = "192.168.1.64"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

################################################################
# Nombres de los personajes en ingles para que sea facil reconocerlos
personajes = ['batman', 'superman', 'wonder woman', 'flash', 'green lantern', 'lex luthor', 'catwoman', 'joker',
              'harley quinn', 'poison ivy']
# Caracteristicas de cada personaje
personajesC = [  # Arreglo bidimiensional
    ["heroe", "rico", "capa", "negro", "sabe pelear", "hombre", "cabello", "cabello corto", "inteligente", "batman"],
    ["heroe", "vuela", "super fuerza", "visión laser", "hombre", "capa", "cabello", "cabello corto", "veloz",
     "superman"],
    ["heroe", "vuela", "mujer", "cabello", "cabello largo", "super fuerza", "lazo", "wonder womam"],
    ["heroe", "veloz", "hombre", "rojo", "agil", "cabello", "cabello corto", "flash"],
    ["heroe", "super fuerte", "verde", "vuela", "hombre", "cabello", "cabello corto", "green lantern"],
    ["villano", "rico", "hombre", "inteligente", "calvo", "lex luthor"],
    ["villano", "mujer", "negro", "sabe pelear", "cabello", "agil", "cabello corto", "catwoman"],
    ["villano", "hombre", "inteligente", "payaso", "cabello", "joker"],
    ["villano", "mujer", "cabello", "cabello largo", "sabe pelear", "payaso", "agil", "harley quinn"],
    ["villano", "mujer", "cabello", "cabello largo", "agil", "verde", "poison ivy"]
]


#######################################################################
def verPersonajes():
    global personajes, personajesC
    print("******PERSONAJES******")
    for i in range(0, len(personajes)):
        print("{}:\t{}".format(personajes[i], personajesC[i]))
    print("**********************")


def GrabarPregunta():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = 3
    filename = "audio.wav"

    p = pyaudio.PyAudio()

    print('Grabando')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    print('Terminando de grabar')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Bienvenido a Memoria")

    TCPClientSocket.sendall(b" ")
    data = TCPClientSocket.recv(buffer_size)
    Jugador = data.decode()
    if (data.decode() == "JH"):  # Código para jugador host
        numPlay = input("Ingrese el número de jugadores: \n")
        TCPClientSocket.sendall(numPlay.encode())
        data = TCPClientSocket.recv(buffer_size)  # Manda al servidor el número de jugadores

        TCPClientSocket.sendall(b" ")
        print("Esperando a otros jugadores...")
        data = TCPClientSocket.recv(
            buffer_size)  # Espera a que el servidor mande algo para que sepa que ya se ha cumplido la barrera
        TCPClientSocket.sendall(b" ")

    if (data.decode() == "ETC"):  # Código para otros jugadores
        print("Esperando a otros jugadores...")
        TCPClientSocket.sendall(b" ")
        data = TCPClientSocket.recv(buffer_size)
        TCPClientSocket.sendall(
            b" ")  # Prácticamente solo sincroniza los enviar y recibir, si no luego hace cosas raras xD

        time.sleep(1)

    while True:
        print("Espere su turno: ")
        data = TCPClientSocket.recv(buffer_size)
        verPersonajes()
        coord = input("Pulse enter para grabar ")
        # TCPClientSocket.sendall(coord.encode())
        ##########################################
        GrabarPregunta()
        TamAud = Path("audio.wav").stat().st_size
        # print(str(TamAud))
        TCPClientSocket.sendall(str(TamAud).encode())
        with open("audio.wav", 'rb') as f:
            for l in f:
                TCPClientSocket.sendall(l)
        print("Terminando de enviar archivo")
        respuesta = TCPClientSocket.recv(buffer_size)
        print(respuesta.decode())
