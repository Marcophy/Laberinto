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

import lab_functions as lb

# ****** Initial variables ******
map_path = 'map_01.map'

number_of_generations = 1000
life_per_generation = 100
team_size = 10
mutation_prob = 0.05

# ****** MAIN ******
# Clean terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Load map from file
map_array = np.loadtxt(map_path, comments="#", delimiter=" ", unpack=False)
map_size = np.shape(map_array)
goal_location = (np.where(map_array == 9)[0][0], np.where(map_array == 9)[1][0])
ini_location = (np.where(map_array == 2)[0][0], np.where(map_array == 2)[1][0])
steps_limit = map_size[0] * map_size[1]

fitness_progression = []

population_paths = lb.initial_population(map_array, life_per_generation)
fitness_progression.append(lb.best_worse(population_paths)[0])

for generation in range(number_of_generations):
    print('GENERATION = ', generation + 1)

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
    best, worst = lb.best_worse(population_paths)
    fitness_progression.append(best)

    print(f"{best:.4f} - {worst:.4f}")

# Plot results
map_array[map_array == 2] = 0  # Remove the initial position of the NPC
map_array[map_array == 9] = 0  # Remove the position of the goal
map_array[map_array == 1] = -1  # Rescale the walls

alpha_index = min(range(len(population_paths)), key=lambda i: population_paths[i][0])

fig = plt.figure(layout='constrained', figsize=(12, 6))






print('END')
