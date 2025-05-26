import pandas as pd
import numpy as np

# 1) Leer el archivo CSV c
df = pd.read_csv('notas_parciales.csv', sep=';')

# 2) Calcular promedio de cada alumno
df['Promedio'] = df[['Parcial1', 'Parcial2', 'Parcial3']].mean(axis=1)

# 3) Definir la función de aptitud
def fitness(promedios):
    aprobados = np.sum(promedios >= 11)
    porcentaje_aprobados = aprobados / len(promedios)
    promedio_general = np.mean(promedios)

    # Penaliza si el promedio general supera 14
    if promedio_general > 14:
        return porcentaje_aprobados - (promedio_general - 14) * 0.1
    else:
        return porcentaje_aprobados

# Variables para encontrar el mejor offset
mejor_offset = 0
mejor_fitness = -np.inf
mejor_promedios = df['Promedio']

# 4) Probar offsets aleatorios de -2.0 a +2.0 en pasos de 0.5
for offset in np.arange(-2.0, 2.5, 0.5):
    nuevos_promedios = df['Promedio'] + offset
    nuevos_promedios = nuevos_promedios.clip(0, 20)  
    f = fitness(nuevos_promedios)

    if f > mejor_fitness:
        mejor_fitness = f
        mejor_offset = offset
        mejor_promedios = nuevos_promedios

# 5) Mostrar resultados
print(f"\nOffset óptimo encontrado: {mejor_offset}")
print(f"Aptitud final: {mejor_fitness:.4f}")

# Mostrar nueva distribución de notas
df['Promedio Ajustado'] = mejor_promedios.round(2)
df['Estado'] = df['Promedio Ajustado'].apply(lambda x: 'Aprobado' if x >= 11 else 'Desaprobado')
print("\nDistribución final de notas:\n")
print(df[['StudentID', 'Promedio', 'Promedio Ajustado', 'Estado']].head(15))  # Mostrar primeros 15
