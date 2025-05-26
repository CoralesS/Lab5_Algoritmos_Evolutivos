import pandas as pd
import random

# Leer matriz de distancias
df = pd.read_csv('distancias_labs.csv', index_col=0, delimiter=';')
labs = list(df.columns)

# Convertir a matriz numpy para acceso rápido
dist_matrix = df.values

def distancia_total(ruta, matriz):
    distancia = 0
    n = len(ruta)
    for i in range(n - 1):
        distancia += matriz[ruta[i], ruta[i+1]]
    # Volver al inicio (opcional)
    distancia += matriz[ruta[-1], ruta[0]]
    return distancia

def obtener_vecinos(ruta):
    vecinos = []
    n = len(ruta)
    for i in range(n):
        for j in range(i+1, n):
            vecino = ruta.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]  # intercambio
            vecinos.append(vecino)
    return vecinos

def hill_climbing(matriz, iteraciones=1000):
    n = len(matriz)
    # Solución inicial aleatoria
    mejor_ruta = list(range(n))
    random.shuffle(mejor_ruta)
    mejor_distancia = distancia_total(mejor_ruta, matriz)

    for _ in range(iteraciones):
        vecinos = obtener_vecinos(mejor_ruta)
        mejor_vecino = None
        mejor_distancia_vecino = mejor_distancia

        for vecino in vecinos:
            dist = distancia_total(vecino, matriz)
            if dist < mejor_distancia_vecino:
                mejor_vecino = vecino
                mejor_distancia_vecino = dist

        if mejor_vecino is None:
            break  # No hay mejor vecino, óptimo local
        else:
            mejor_ruta = mejor_vecino
            mejor_distancia = mejor_distancia_vecino

    return mejor_ruta, mejor_distancia

# Ejecutar hill climbing
ruta_optima, distancia_optima = hill_climbing(dist_matrix)

# Mostrar resultados
print("Ruta óptima de laboratorios a visitar (orden):")
print(" -> ".join(labs[i] for i in ruta_optima))
print(f"Distancia total caminando (metros): {distancia_optima:.2f}")

