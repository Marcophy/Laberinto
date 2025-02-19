# ****** Modules ******
import numpy as np
import random
from tqdm import tqdm


# ****** Functions ******
def select_new_step():
    """
    Function to generate a new step
    :return:
        int: 0=Right, 1=Up, 2=Left, 3=Down
    """

    num = np.random.rand()

    if num < 0.25:
        return 0
    elif num < 0.5:
        return 1
    elif num < 0.75:
        return 2
    else:
        return 3


def check_step(in_array, in_location, in_mode='wall'):
    """
    Check if the new step is valid.

    Args:
        in_array (numpy.ndarray): Full map array
        in_location (list): New location
        in_mode (str): Define the type of detection:
            'wall': Detect if the NPC hits a wall
            'wall_plot': Detect if the NPC hits a wall during the results plotting
            'goal': Detect if the NPC achieves the goal

    Returns:
        bool:
    """

    if in_mode == 'wall':
        if in_array[in_location[0], in_location[1]] == 1:
            return False
        else:
            return True

    if in_mode == 'wall_plot':
        if in_array[in_location[0], in_location[1]] == -1:
            return False
        else:
            return True

    elif in_mode == 'goal':
        if in_array[in_location[0], in_location[1]] == 9:
            return True
        else:
            return False
    else:
        print('ERROR')
        exit()


def calculate_fitness(in_map, in_path):
    map_size = np.shape(in_map)
    goal_location = (np.where(in_map == 9)[0][0], np.where(in_map == 9)[1][0])
    location = (np.where(in_map == 2)[0][0], np.where(in_map == 2)[1][0])

    for item in in_path:
        # Check the new step
        if item == 0:  # Right
            temp_location = (location[0], location[1] + 1)
        elif item == 1:  # Up
            temp_location = (location[0] - 1, location[1])
        elif item == 2:  # Left
            temp_location = (location[0], location[1] - 1)
        else:  # Down
            temp_location = (location[0] + 1, location[1])

        if check_step(in_map, temp_location, 'wall'):
            location = temp_location

    d = abs(goal_location[0] - location[0]) + abs(goal_location[1] - location[1])
    if d == 0:
        return int(3 * (map_size[0] * map_size[1]) - len(in_path))
    else:
        return float(1 / (1 + d))


def initial_population(in_map_array, in_life_per_generation):
    map_size = np.shape(in_map_array)
    ini_location = (int(np.where(in_map_array == 2)[0][0]), int(np.where(in_map_array == 2)[1][0]))
    steps_limit = map_size[0] * map_size[1]

    initial_population_paths = []
    for life in tqdm(range(in_life_per_generation), desc="First generation", ncols=100):
        life_path = []
        current_location = ini_location
        control = True
        cnt_step = 0
        while control:
            # Select the new step
            new_step = select_new_step()
            life_path.append(new_step)

            # Check the new step
            if new_step == 0:  # Right
                temp_location = (current_location[0], current_location[1] + 1)
            elif new_step == 1:  # Up
                temp_location = (current_location[0] - 1, current_location[1])
            elif new_step == 2:  # Left
                temp_location = (current_location[0], current_location[1] - 1)
            else:  # Down
                temp_location = (current_location[0] + 1, current_location[1])

            if check_step(in_map_array, temp_location, 'wall'):
                current_location = temp_location
                if check_step(in_map_array, current_location, 'goal'):
                    life_path.insert(0, calculate_fitness(in_map_array, life_path))
                    control = False

            cnt_step += 1
            if cnt_step > steps_limit:
                life_path.insert(0, calculate_fitness(in_map_array, life_path))
                control = False

        initial_population_paths.append(life_path)

    return initial_population_paths


def tournament_selection(in_population_paths, in_team_size):
    # First candidate
    for player in range(in_team_size):
        index = random.randint(0, len(in_population_paths) - 1)
        if player == 0:
            first_best_path = in_population_paths[index]
        else:
            if in_population_paths[index][0] > first_best_path[0]:
                first_best_path = in_population_paths[index]

    # Second candidate
    for player in range(in_team_size):
        index = random.randint(0, len(in_population_paths) - 1)
        if player == 0:
            second_best_path = in_population_paths[index]
        else:
            if in_population_paths[index][0] > second_best_path[0]:
                second_best_path = in_population_paths[index]

    return first_best_path, second_best_path


def crossover(in_first, in_second):
    cut_first = random.randint(0, len(in_first) - 1)
    cut_second = random.randint(0, len(in_second) - 1)

    new_child = in_first[1:cut_first] + in_second[cut_second:]
    return list(new_child)


def mutation(in_child, in_mutation_prob):
    for index in range(len(in_child)):
        if np.random.rand() < in_mutation_prob:
            in_child[index] = random.randint(0, 3)
    return in_child


def survivor_selection(in_population_paths, in_child):
    weak_member = min(range(len(in_population_paths)), key=lambda i: in_population_paths[i][0])

    in_population_paths[weak_member] = in_child

    return in_population_paths


def best_worse(in_population_paths, in_mode='value'):
    best_value = -1
    worse_value = 3

    best_index = -1
    worse_index = -1

    cnt = 0
    for item in in_population_paths:
        if item[0] > best_value:
            best_value = item[0]
            best_index = cnt

        if item[0] < worse_value:
            worse_value = item[0]
            worse_index = cnt

        cnt += 1

    if in_mode == 'value':
        return best_value, worse_value
    elif in_mode == 'index':
        return best_index, worse_index
    else:
        print('Error')
        exit()


def update_map(in_map_array, in_population_paths):
    ini_location = (int(np.where(in_map_array == 2)[0][0]), int(np.where(in_map_array == 2)[1][0]))
    goal_location = (int(np.where(in_map_array == 9)[0][0]), int(np.where(in_map_array == 9)[1][0]))

    # Clean the initial map
    in_map_array[in_map_array == 1] = -1  # Rescale the walls

    best_index = best_worse(in_population_paths, 'index')
    best_path = in_population_paths[best_index[0]]
    best_path.pop(0)

    current_location = ini_location
    for item in best_path:
        # Check the new step
        if item == 0:  # Right
            temp_location = (current_location[0], current_location[1] + 1)
        elif item == 1:  # Up
            temp_location = (current_location[0] - 1, current_location[1])
        elif item == 2:  # Left
            temp_location = (current_location[0], current_location[1] - 1)
        else:  # Down
            temp_location = (current_location[0] + 1, current_location[1])

        if check_step(in_map_array, temp_location, 'wall_plot'):
            current_location = temp_location
            # in_map_array[current_location] = 1

        in_map_array[current_location] += 1

    in_map_array[ini_location] = -2
    in_map_array[goal_location] = -3

    return in_map_array

