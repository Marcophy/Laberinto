"""
LABERINTO solves a labyrinth using a genetic algorithm.
Marco A. Villena, PhD.
2023 - 2025
"""

# ****** dunder variables ******
__project_name__ = "Labyrinth genetic algorithm"
__author__ = "Marco A. Villena"
__email__ = "mavillena@ugr.es"
__project_date__ = "2023 - 2025"
__version__ = "1.0"

# ****** Modules ******
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
from datetime import datetime

import lab_functions as lb

# ****** Initial variables ******
# User variables
map_path = 'map_01.map'  # See Maps folder
number_of_generations = 10000
live_per_generation = 1000
team_size = 10  # Team size of the tournament selection method.
mutation_prob = 0.05  # Mutation probability

# Internal variables
output_plot = map_path.replace(".map", ".jpg")
output_file = 'results_database.txt'

# ****** MAIN ******
# Clean terminal
os.system('cls' if os.name == 'nt' else 'clear')
work_folder = os.getcwd()

initial_time = time.time()

# Load map from file
map_array = np.loadtxt(os.path.join(work_folder, 'Maps', map_path), comments="#", delimiter=" ", unpack=False, dtype='int')
map_size = np.shape(map_array)
goal_location = (int(np.where(map_array == 9)[0][0]), int(np.where(map_array == 9)[1][0]))
ini_location = (int(np.where(map_array == 2)[0][0]), int(np.where(map_array == 2)[1][0]))

steps_limit = int(2 * map_size[0] * map_size[1])

fitness_progression = []

# Generation of the first population
print('Generating initial population ...')
time.sleep(1)

population_paths = lb.initial_population(map_array, live_per_generation)
fitness_progression.append(lb.best_worse(population_paths)[0])
best, worst = lb.best_worse(population_paths, 'value')

print(f"First generation generated.\n\t{best:.4f} - {worst:.4f}")
time.sleep(1)

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
    child.insert(0, lb.calculate_fitness(map_array, child, steps_limit))

    # Survivor selection
    population_paths = lb.survivor_selection(population_paths, child)

    # Show results
    best, worst = lb.best_worse(population_paths, 'value')
    fitness_progression.append(best)

print(f"Last generation.\n\t{best:.4f} - {worst:.4f}")

final_time = time.time()
print(f"\nExecution time: {final_time - initial_time:.3f} seconds")

# Export data
best, worst = lb.best_worse(population_paths, 'index')
best_path = population_paths[best]

fitness_score = best_path[0]
if fitness_score > 1:
    fitness_score = str(fitness_score)
else:
    fitness_score = f"{fitness_score:.5f}"

best_path.pop(0)
best_path = "".join(map(str, best_path))

sim_time = final_time - initial_time
if sim_time < 300:
    sim_time = f"{sim_time:.2f}".zfill(8)
else:
    sim_time = str(int(sim_time)).zfill(8)
output = datetime.now().strftime("%Y-%m-%d %H:%M") + '\t' + map_path + '\t\t' + sim_time + '\t' + fitness_score + '\t\t' + str(len(best_path)) + '\t\t\t' + best_path


with open(os.path.join(work_folder, 'Outputs', output_file), "a", encoding="utf-8") as file:
    file.write(output + "\n")

# Plot results
updated_map = lb.update_map(map_array, population_paths)

# Crear la figura con dos paneles
fig, axes = plt.subplots(1, 2, figsize=(25, 12))  # 1 fila, 2 columnas

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
output_plot = datetime.now().strftime("%Y-%m-%d_%H-%M") + '_' + output_plot
plt.savefig(os.path.join(work_folder, 'Outputs', output_plot), dpi=300)
plt.show()

print('END')
