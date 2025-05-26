import pandas as pd
import random

# Leer el archivo CSV 
df = pd.read_csv('preguntas.csv', sep=';')

def fitness(solution, df):
    total_time = sum(df['Time_min'][i] for i, val in enumerate(solution) if val == 1)
    total_diff = sum(df['Difficulty'][i] for i, val in enumerate(solution) if val == 1)
    
    # Penalizar si no cumple las restricciones
    if total_time > 90 or total_diff < 180 or total_diff > 200:
        return -float('inf')
    return total_diff

def get_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution.copy()
        neighbor[i] = 1 - neighbor[i]  
        neighbors.append(neighbor)
    return neighbors

def hill_climbing(df, max_iter=1000):
    n = len(df)
    # Solución inicial aleatoria
    current = [random.choice([0, 1]) for _ in range(n)]
    current_score = fitness(current, df)
    
    for _ in range(max_iter):
        neighbors = get_neighbors(current)
        neighbor_scores = [fitness(nb, df) for nb in neighbors]
        
        max_score = max(neighbor_scores)
        if max_score <= current_score:
            break  # No hay mejora
        
        current = neighbors[neighbor_scores.index(max_score)]
        current_score = max_score
    
    return current, current_score

# Ejecutar hill climbing
solution, score = hill_climbing(df)

# Resultados
selected_questions = [df['QuestionID'][i] for i, val in enumerate(solution) if val == 1]
total_time = sum(df['Time_min'][i] for i, val in enumerate(solution) if val == 1)

print("Preguntas seleccionadas:", selected_questions)
print("Dificultad total:", score)
print("Tiempo total (min):", total_time)

