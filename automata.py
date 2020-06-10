import random
import time


def validarBatman(pregunta):
    estado='q0'
    for i in range(0,len(pregunta)):
        print(pregunta[i])
        estado=Batman[(estado,pregunta[i])]

    if (
        estado == 'q5' or
        estado == 'q6' or
        estado == 'q8' or
        estado == 'q10' or
        estado == 'q11' or
        estado == 'q13' or
        estado == 'q16'
       ):
        return "Si"
    elif estado == 'q9':
        return "Correcto"
    else:
        return "No"

Batman = {
    ('q0', "tu"): 'q1', 
    ('q1', 'personaje'): 'q2',
    ('q2', 'es'): 'q3',
    ('q2', 'tiene'): 'q7',
    ('q2', 'sabe'): 'q12',
    ('q2', 'viste'): 'q14',
    ('q3', 'un'): 'q4',
    ('q3', 'heroe'): 'q5',
    ('q3', 'rico'): 'q6',
    ('q3', 'batman'): 'q9',
    ('q7', 'ropa'): 'q10',
    ('q7', 'capa'): 'q8',
    ('q10', 'negra'): 'q11',
    ('q12', 'pelear'): 'q13',
    ('q14', 'de'): 'q15',
    ('q15', 'negro'): 'q16',
    }

pregunta = input("Ingrese pregunta")
print(validarBatman(pregunta.split()))

