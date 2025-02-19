"""
Laberinto
"""

__project_name__ = "Labyrinth genetic algorithm"
__author__ = "Marco A. Villena"
__email__ = "mavillena@ugr.es"
__project_date__ = "22/04/2023"
__version__ = "1.0"

# ****** Modules ******
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import sleep

import lab_functions as lb

# ****** Initial variables ******
map_path = 'map_04.map'

number_of_generations = 100000
life_per_generation = 10000
team_size = 10
mutation_prob = 0.05

# ****** MAIN ******
# Clean terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Load map from file
map_array = np.loadtxt(map_path, comments="#", delimiter=" ", unpack=False, dtype='int')
map_size = np.shape(map_array)
goal_location = (int(np.where(map_array == 9)[0][0]), int(np.where(map_array == 9)[1][0]))
ini_location = (int(np.where(map_array == 2)[0][0]), int(np.where(map_array == 2)[1][0]))

steps_limit = int(2 * map_size[0] * map_size[1])

fitness_progression = []

# Generation of the first population
print('Generating initial population ...')
sleep(1)

population_paths = lb.initial_population(map_array, life_per_generation)
fitness_progression.append(lb.best_worse(population_paths)[0])
best, worst = lb.best_worse(population_paths, 'value')

print(f"First generation generated.\n\t{best:.4f} - {worst:.4f}")
if worst < 0:
    print('ERROR')
    exit()
sleep(1)
cnt = 1
for generation in tqdm(range(number_of_generations), desc="Evolution", ncols=100):
    cnt += 1

    # Selection
    first_candidate, second_candidate = lb.tournament_selection(population_paths, team_size)

    # Crossover
    child = lb.crossover(first_candidate, second_candidate)

    # Mutation
    child = lb.mutation(child, mutation_prob)

    # Calculate fitness
    child.insert(0, lb.calculate_fitness(map_array, child))

    # Survivor selection
    population_paths = lb.survivor_selection(population_paths, child)

    # Show results
    best, worst = lb.best_worse(population_paths, 'value')
    fitness_progression.append(best)

print(f"Last generation.\n\t{best:.4f} - {worst:.4f}")


# Plot results
updated_map = lb.update_map(map_array, population_paths)

# Crear la figura con dos paneles
fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 1 fila, 2 columnas

# Panel izquierdo: imshow de la array
im = axes[0].imshow(updated_map.tolist(), cmap="Greys", aspect="auto")
plt.colorbar(im, ax=axes[0])  # Añadir barra de color

# Panel derecho: Gráfica de la lista
axes[1].plot(fitness_progression, linestyle="-", marker="")  # Línea continua sin puntos
axes[1].set_xlim(left=0)  # Forzar que el eje x empiece en 0
axes[1].set_ylim(bottom=0)  # Forzar que el eje y empiece en 0
axes[1].set_xlabel("# Generation")
axes[1].set_ylabel("Fitness")


# Mostrar la figura
plt.tight_layout()
plt.show()

print('END')
