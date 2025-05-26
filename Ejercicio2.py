import pandas as pd
import random

# Leer archivo CSV
df = pd.read_csv('disponibilidad.csv', delimiter=';')

# Convertimos la tabla de disponibilidad en diccionario
disponibilidad = {}
slots = df.columns[1:]  

for idx, row in df.iterrows():
    mentor = row['MentorID']
    # slots donde mentor está disponible
    disponibles = [slot for slot in slots if row[slot] == 1]
    disponibilidad[mentor] = disponibles

mentores = list(disponibilidad.keys())

def calcular_choques(asignacion):
    # contar cuántos slots están asignados a más de un mentor
    slot_ocupados = {}
    choques = 0
    for mentor, slot in asignacion.items():
        if slot not in slot_ocupados:
            slot_ocupados[slot] = 0
        slot_ocupados[slot] += 1
    for slot, count in slot_ocupados.items():
        if count > 1:
            choques += (count - 1)
    return choques

def solucion_inicial():
    # Asignar aleatoriamente un slot disponible a cada mentor
    asignacion = {}
    for mentor in mentores:
        asignacion[mentor] = random.choice(disponibilidad[mentor])
    return asignacion

def obtener_vecinos(asignacion):
    # Generar vecinos cambiando el slot asignado de un mentor
    vecinos = []
    for mentor in mentores:
        slots_posibles = [s for s in disponibilidad[mentor] if s != asignacion[mentor]]
        for nuevo_slot in slots_posibles:
            vecino = asignacion.copy()
            vecino[mentor] = nuevo_slot
            vecinos.append(vecino)
    return vecinos

def busqueda_local(max_iter=1000):
    asignacion = solucion_inicial()
    mejor_asignacion = asignacion
    mejor_costo = calcular_choques(asignacion)
    iter = 0
    
    while mejor_costo > 0 and iter < max_iter:
        vecinos = obtener_vecinos(mejor_asignacion)
        mejor_vecino = None
        mejor_costo_vecino = mejor_costo
        
        for vecino in vecinos:
            costo = calcular_choques(vecino)
            if costo < mejor_costo_vecino:
                mejor_vecino = vecino
                mejor_costo_vecino = costo
        
        if mejor_vecino is None:
            # No mejor vecino, termina
            break
        else:
            mejor_asignacion = mejor_vecino
            mejor_costo = mejor_costo_vecino
        
        iter += 1
    
    return mejor_asignacion, mejor_costo

# Ejecutar búsqueda local
asignacion_final, choques_final = busqueda_local()

print("Asignación final de horarios por mentor:")
for mentor, slot in asignacion_final.items():
    print(f"{mentor}: {slot}")

print(f"\nNúmero de choques: {choques_final}")
