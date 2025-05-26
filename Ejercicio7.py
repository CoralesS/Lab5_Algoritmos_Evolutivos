import pandas as pd
import numpy as np
import random
from collections import Counter

# Cargar datos
df = pd.read_csv("alumnos.csv", sep=";")

# Mapear habilidades a valores enteros para poder comparar
skill_types = df['Skill'].unique()
skill_map = {skill: idx for idx, skill in enumerate(skill_types)}
df['SkillNum'] = df['Skill'].map(skill_map)

# Parámetros
n_students = len(df)
team_size = 4
n_teams = 5
assert n_students == team_size * n_teams

# Función para calcular la varianza total de GPA y penalización por desequilibrio de habilidades
def fitness(equipos):
    gpa_vars = []
    penalty = 0
    for equipo in equipos:
        gpas = [df.iloc[i]['GPA'] for i in equipo]
        skills = [df.iloc[i]['Skill'] for i in equipo]
        gpa_vars.append(np.var(gpas))
        skill_count = Counter(skills)
        # Penaliza si no hay variedad o si hay mucha diferencia entre skills
        penalty += sum(abs(skill_count[skill] - len(skills)/len(skill_types)) for skill in skill_types)
    return sum(gpa_vars) + penalty  # Queremos minimizar esto

# Inicializar equipos aleatoriamente
def generar_solucion_inicial():
    indices = list(df.index)
    random.shuffle(indices)
    return [indices[i * team_size:(i + 1) * team_size] for i in range(n_teams)]

# Vecino: intercambio de dos alumnos de equipos distintos
def generar_vecino(equipos):
    new_equipos = [list(e) for e in equipos]
    team1, team2 = random.sample(range(n_teams), 2)
    i = random.choice(range(team_size))
    j = random.choice(range(team_size))
    # Intercambiar
    new_equipos[team1][i], new_equipos[team2][j] = new_equipos[team2][j], new_equipos[team1][i]
    return new_equipos

# Algoritmo de hill climbing
def hill_climbing(iteraciones=1000):
    actual = generar_solucion_inicial()
    mejor_fitness = fitness(actual)
    for _ in range(iteraciones):
        vecino = generar_vecino(actual)
        vecino_fitness = fitness(vecino)
        if vecino_fitness < mejor_fitness:
            actual = vecino
            mejor_fitness = vecino_fitness
    return actual, mejor_fitness

# Ejecutar algoritmo
equipos_finales, mejor_score = hill_climbing()

# Mostrar resultados
print("=== Composición de equipos ===")
for idx, equipo in enumerate(equipos_finales, 1):
    print(f"\nEquipo {idx}:")
    for i in equipo:
        estudiante = df.iloc[i]
        print(f"  {estudiante['StudentID']} - GPA: {estudiante['GPA']} - Skill: {estudiante['Skill']}")

# Mostrar métricas
def mostrar_metricas(equipos):
    print("\n=== Métricas por equipo ===")
    for i, equipo in enumerate(equipos, 1):
        gpas = [df.iloc[j]['GPA'] for j in equipo]
        skills = [df.iloc[j]['Skill'] for j in equipo]
        skill_dist = dict(Counter(skills))
        print(f"Equipo {i}: GPA promedio = {np.mean(gpas):.2f}, Varianza = {np.var(gpas):.2f}, Skills = {skill_dist}")
    print(f"\nFitness total (varianza + penalización): {fitness(equipos):.4f}")

mostrar_metricas(equipos_finales)

