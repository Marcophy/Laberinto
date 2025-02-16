# ****** Modules ******
import numpy as np
import random
import matplotlib.pyplot as plt


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


def check_step(in_array, in_location):
    """
    Check if the new step is valid.

    Args:
        in_array (numpy.ndarray): Full map array
        in_location (list): New location

    Returns:
        bool:
    """

    if in_array[in_location[0], in_location[1]] == 1:
        return False
    else:
        return True


def check_goal(in_array, in_location):
    """
    Check if the NPC arrived the goal.

    Args:
        in_array (numpy.ndarray): Full map array
        in_location (list): New location

    Returns:
        bool:
    """

    if in_array[in_location[0], in_location[1]] == 9:
        return True
    else:
        return False


def calculate_fitness(in_map, in_path):
    map_size = np.shape(in_map)
    goal_location = (np.where(in_map == 9)[0][0], np.where(in_map == 9)[1][0])
    location = (np.where(in_map == 2)[0][0], np.where(in_map == 2)[1][0])
    steps_limit = map_size[0] * map_size[1]

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

        if check_step(in_map, temp_location):
            location = temp_location

    d = abs(goal_location[0] - location[0]) + abs(goal_location[1] - location[1])
    if d == 0:
        return (map_size[0] * map_size[1]) - len(in_path)
    else:
        return 1 / (1 + d)


def initial_population(in_map_array, in_life_per_generation):
    map_size = np.shape(in_map_array)
    #  goal_location = (np.where(in_map_array == 9)[0][0], np.where(in_map_array == 9)[1][0])
    ini_location = (np.where(in_map_array == 2)[0][0], np.where(in_map_array == 2)[1][0])
    steps_limit = map_size[0] * map_size[1]

    initial_population_paths = []
    for life in range(in_life_per_generation):
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

            if check_step(in_map_array, temp_location):
                current_location = temp_location
                if check_goal(in_map_array, current_location):
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


def best_worse(in_population_paths):
    best = -1
    worse = 3
    for item in in_population_paths:
        if item[0] > best:
            best = item[0]
        if item[0] < worse:
            worse = item[0]

    return best, worse


def plot_results(in_generation, in_history, in_alpha, in_map, in_right, in_up, in_left, in_down, in_cmap='viridis'):
    """
    Plot all results about probabilities, the best path, and Score history in the same panel. The result is saved as PNG picture.

    Args:
        in_generation (str): Total number of generations simulated
        in_history (list): List of all score obtained by each generation simulates
        in_alpha (list): List with all steps followed for the alpha life [row, column, step direction]
        in_map (numpy.ndarray): Map of the labyrinth
        in_right (numpy.ndarray): Step probability map to move in the right direction.
        in_up (numpy.ndarray): Step probability map to move in the up direction.
        in_left (numpy.ndarray): Step probability map to move in the left direction.
        in_down (numpy.ndarray): Step probability map to move in the down direction.
        in_cmap (str): Color map used for the figures

    Returns: NONE
    """

    file_name = 'generation_' + str(in_generation) + '.png'  # Name of the output file

    # Record the winner path in the map
    in_map[in_map == 2] = 0  # Remove the initial position of the NPC
    in_map[in_map == 9] = 0  # Remove the position of the goal
    for step in range(len(in_alpha)):
        in_map[tuple(in_alpha[step][0:2])] += 1

    # Create a figure structure with 2x1 main panels
    fig = plt.figure(layout='constrained', figsize=(12, 6))
    subfigs = fig.subfigures(1, 2, wspace=0.07, width_ratios=[2, 1])

    # Figures placed in the left panel
    axsleft = subfigs[0].subplots(2, 2, sharex=True, sharey=True)
    subfigs[0].set_facecolor('0.95')

    axsleft[0, 0].set_title('Right')
    axsleft[0, 1].set_title('Up')
    axsleft[1, 0].set_title('Left')
    axsleft[1, 1].set_title('Down')

    pnl1 = axsleft[0, 0].imshow(in_right, cmap=in_cmap, interpolation='nearest', vmin=0, vmax=1)
    axsleft[0, 1].imshow(in_up, cmap=in_cmap, interpolation='nearest', vmin=0, vmax=1)
    axsleft[1, 0].imshow(in_left, cmap=in_cmap, interpolation='nearest', vmin=0, vmax=1)
    axsleft[1, 1].imshow(in_down, cmap=in_cmap, interpolation='nearest', vmin=0, vmax=1)
    subfigs[0].colorbar(pnl1, shrink=0.6, ax=axsleft, location='bottom')

    # Figures placed in the right panel
    axsright = subfigs[1].subplots(2, 1, sharex=False, sharey=False)
    axsright[0].set_title('Best path')
    axsright[1].set_title('Score each generation')
    axsright[1].set_xlabel('Generation')
    axsright[1].set_ylabel('Score')

    pnl5 = axsright[0].imshow(in_map, cmap=in_cmap, interpolation='nearest', vmin=0)
    plt.colorbar(pnl5, ax=axsright[0], shrink=0.6, location='bottom')
    axsright[1].plot(list(in_history), '.-')

    # Show the graph
    plt.savefig(file_name, dpi=300)
