# Labyrinth heatmap - addon
# This addon allows to plot all results stored in the output files fo Labyrinth heatmap.

__project_name__ = "Plot path"
__author__ = "Marco A. Villena"
__email__ = "mavillena@ugr.es"
__project_date__ = "23/04/2023"

# ****** Modules ******
import os
from lab_functions import plot_results
import numpy as np

# ****** Initial variables ******
map_file = 'map_01.map'
alpha_file = 'alpha_history.txt'
winner_file = 'winner_path.txt'
pright_file = 'prob_right.txt'
pup_file = 'prob_up.txt'
pleft_file = 'prob_left.txt'
pdown_file = 'prob_down.txt'

# ****** MAIN ******
# Clean terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Load map from file
map_array = np.loadtxt(map_file, comments="#", delimiter=" ", unpack=False)
alpha_history = list(np.loadtxt(alpha_file, comments="#", delimiter=" ", unpack=False))
winner_life = np.loadtxt(winner_file, comments="#", delimiter=" ", unpack=False).astype(int).tolist()
prob_right = np.loadtxt(pright_file, comments="#", delimiter=" ", unpack=False)
prob_up = np.loadtxt(pup_file, comments="#", delimiter=" ", unpack=False)
prob_left = np.loadtxt(pleft_file, comments="#", delimiter=" ", unpack=False)
prob_down = np.loadtxt(pdown_file, comments="#", delimiter=" ", unpack=False)

generation = str(len(alpha_history))

plot_results(generation, alpha_history, winner_life, map_array, prob_right, prob_up, prob_left, prob_down, 'hot')

print('END')
