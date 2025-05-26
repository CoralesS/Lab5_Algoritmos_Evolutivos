import pandas as pd
import random
import math

# Leer datos de proyectos
df = pd.read_csv('proyectos.csv', delimiter=';')
proyectos = df['ProjectID'].tolist()
costos = df['Cost_Soles'].tolist()
beneficios = df['Benefit_Soles'].tolist()
presupuesto = 10000

# Función de aptitud: beneficio si costo ≤ presupuesto, -inf si no
def fitness(bitstring):
    costo_total = 0
    beneficio_total = 0
    for i, bit in enumerate(bitstring):
        if bit == '1':
            costo_total += costos[i]
            beneficio_total += beneficios[i]
    if costo_total > presupuesto:
        return -math.inf
    else:
        return beneficio_total

# Generar vecinos
def obtener_vecinos(bitstring):
    vecinos = []
    for i in range(len(bitstring)):
        bit = bitstring[i]
        nuevo_bit = '0' if bit == '1' else '1'
        vecino = bitstring[:i] + nuevo_bit + bitstring[i+1:]
        vecinos.append(vecino)
    return vecinos

def hill_climbing(iteraciones=1000):
    # Solución inicial aleatoria
    actual = ''.join(random.choice(['0','1']) for _ in range(len(proyectos)))
    mejor = actual
    mejor_fitness = fitness(mejor)

    for _ in range(iteraciones):
        vecinos = obtener_vecinos(actual)
        mejor_vecino = None
        mejor_fitness_vecino = mejor_fitness

        for vecino in vecinos:
            f = fitness(vecino)
            if f > mejor_fitness_vecino:
                mejor_vecino = vecino
                mejor_fitness_vecino = f

        if mejor_vecino is None:
            break  # óptimo local
        else:
            actual = mejor_vecino
            mejor_fitness = mejor_fitness_vecino
            mejor = mejor_vecino

    return mejor, mejor_fitness

# Ejecutar hill climbing
solucion_optima, beneficio_optimo = hill_climbing()

# Mostrar resultados
proyectos_seleccionados = [proyectos[i] for i, bit in enumerate(solucion_optima) if bit == '1']
print("Proyectos seleccionados:")
print(proyectos_seleccionados)
print(f"Beneficio total estimado: S/ {beneficio_optimo}")

