# LABERINTO
*Author: [**Marco A. Villena**](https://www.marcoavillena.com/)*

[LABERINTO](https://github.com/Marcophy/Laberinto) automatically solves any 2D labyrinth using a **Genetic Algorith**.

*DISCLAIMER*: This script is for training and testing purposes only, so some conceptual errors might be found and many improvements can be considered. 

---

# Theoretical explanation
A **Genetic Algorithm** is an optimization technique inspired by natural selection. We'll use it to find a path through a labyrinth where the possible movements are **up, down, left, and right**. Below is a step-by-step explanation of how to implement it.

## **1. Define the Problem Representation**  
The labyrinth can be represented as a **grid (matrix)** where:  
- `0` = Open path  
- `1` = Wall (not passable)  
- `2` = Start position  
- `9` = Exit position  

### **Chromosome Representation**  
Each individual (solution) in the population represents a **sequence of movements** (up, down, left, right) from the start position.  
We encode movements as:
- `0` (Right) 
- `1` (Up)
- `2` (Left) 
- `3` (Down)  

A chromosome could be a string like `"0011223300"` (sequence of moves).

## **2. Initialize the Population**  
Generate **N random individuals**, where each chromosome is a sequence of random moves of length **L**.  
Example for `N=5`:  
  - `"0011223300"`  
  - `"2230013202"`  
  - `"1201330012"`  

## **3. Fitness Function**  
The **fitness function** evaluates how close an individual is to the exit. We define it as:  

$\text{Fitness} = \frac{1}{1 + d}$

Where:  
- \( d \) = **Manhattan distance** from the final position of the sequence to the exit.  
- If the sequence reaches the exit exactly, give it a high fitness score (e.g., `1000`).  

## **4. Selection**  
Select parents using **Tournament Selection** or **Roulette Wheel Selection**:  
- **Tournament Selection**: Pick `k` random individuals and select the one with the best fitness.  
- **Roulette Wheel**: Assign a probability to each individual based on fitness and select probabilistically.  

## **5. Crossover (Recombination)**  
Combine two parent chromosomes to create offspring.  
- **One-Point Crossover**:  
  - Choose a random crossover point.  
  - Swap segments from parents.  

  **Example:**  
  - Parent 1: `"2230013202"`  
  - Parent 2: `"1201330012"`  
  - Crossover at position 4 → Child: `"2230330012"`  

## **6. Mutation**  
With a small probability (e.g., `5%`), randomly mutate a gene (change a move).  
Example:  
  - `"2230330012"` → Mutation at position 3 → `"2200330012"`  

## **7. Survival Selection**  
- Replace the worst-performing individuals with the new offspring.  
- Keep the best solution found so far (**elitism**).  

## **8. Stopping Condition**  
Stop when:  
- An individual **reaches the exit**.  
- A maximum number of generations is reached. 

---

# How to use LABERINTO
To use the [LABERINTO](https://github.com/Marcophy/Laberinto), you need to run the **main.py** file. However, you must initially configure a number of parameters included directly in the code. These parameters are included at the beginning of the script in the section called **Initial Variables**. These variables are:
- `map_path` = Name of the map you want to use (*Ex. 'map_01.map'*). All maps are placed in the *Maps* folder.
- `number_of_generations` = Number of generations (*Ex. 10000*).
- `live_per_generation` = Number of people in each generation (*Ex. 1000*).
- `team_size` = Size of the team of the tournament selection method (*Ex. 10*). *Note: See theoretical section*
- `mutation_prob` = Mutation probability (*Ex. 0.05*)

Once the calculations are finished, the map with the best path found and the evolution of the fitness score are shown. At the same time, this figure will be saved in the **Output** folder. The information related to the result will be saved in the file **results_database.txt** located in the same folder.

## Maps generation
Maps are generated as plain text files with the extension **.map**. Each cell of the map matrix is defined in the file, separated by a blank space. Each cell can contain the following elements:
- `0` = Open path  
- `1` = Wall (not passable)  
- `2` = Start position  
- `9` = Exit position  

All maps must meet the following conditions:
- The outer edge of each map must always be defined as walls.
- The *Start position* and the *Exit position* must be defined.
- A route that connect the *Start position* and the *Exit position* must exist.

*Tip: To facilitate the generation of maps, an Excel file is included in the **Maps** folder.*

---

# Dependencies
[LABERINTO](https://github.com/Marcophy/Laberinto) was developed using [Python v3.12](https://www.python.org/downloads/release/python-3120/). This is the list of non-standard libraries used by this code.
- [Numpy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [tqdm](https://github.com/tqdm/tqdm)

 

