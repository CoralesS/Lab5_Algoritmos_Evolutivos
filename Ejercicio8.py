import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
import random

# Cargar dataset
data = pd.read_csv("HousePricesUNS.csv")
X = data.drop(columns=["Price"])
y = data["Price"]

# Separar datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear entorno DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar RMSE
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Rango de alpha
toolbox.register("attr_alpha", lambda: random.uniform(0.01, 100))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_alpha, 1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de evaluación
def eval_ridge(individual):
    alpha = individual[0]
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    return (rmse,)

toolbox.register("evaluate", eval_ridge)

# Mutación gaussiana 
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.0, indpb=1.0)
toolbox.register("select", tools.selBest)

# Configuración de la búsqueda
population = toolbox.population(n=20)
NGEN = 30  # Número de iteraciones 
convergence = []

# Algoritmo hill climbing 
for gen in range(NGEN):
    offspring = []
    for ind in population:
        mutant = toolbox.clone(ind)
        toolbox.mutate(mutant)
        mutant.fitness.values = toolbox.evaluate(mutant)
        if mutant.fitness.values[0] < ind.fitness.values[0]:  # Mejor vecino
            offspring.append(mutant)
        else:
            offspring.append(ind)
    population[:] = offspring
    fits = [ind.fitness.values[0] for ind in population]
    best_rmse = min(fits)
    convergence.append(best_rmse)
    print(f"Generación {gen+1}: Mejor RMSE = {best_rmse:.4f}")

# Mejor individuo
best_ind = tools.selBest(population, 1)[0]
print("\nMejor α encontrado:", best_ind[0])
print("Mejor RMSE:", eval_ridge(best_ind)[0])

# Curva de convergencia
plt.plot(convergence)
plt.title("Convergencia del RMSE")
plt.xlabel("Generación")
plt.ylabel("RMSE")
plt.grid(True)
plt.show()

