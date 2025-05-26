import random
import time
from utils import is_safe, count_attacking_pairs

# --- الگوریتم پس‌گرد (Backtracking) ---
def solve_n_queens_backtracking(n):
    solutions = []
    board = [-1] * n

    def backtrack(row):
        if row == n:
            solutions.append(list(board)) # یک کپی از راه‌حل اضافه شود
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1 # Backtrack

    start_time = time.time()
    backtrack(0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return solutions[0] if solutions else None, elapsed_time, len(solutions)


# --- الگوریتم ژنتیک (Genetic Algorithm) ---
def solve_n_queens_genetic(n, population_size=100, generations=500, mutation_rate=0.1, patience=50):
    start_time = time.time()

    def initialize_population(n_pop, size_n):
        population = []
        for _ in range(n_pop):
            chromosome = list(range(size_n))
            random.shuffle(chromosome)
            population.append(chromosome)
        return population

    def calculate_fitness(chromosome):
        return -count_attacking_pairs(chromosome)

    def selection(population, fitness_scores):
        tournament_size = 5
        selected = []
        for _ in range(len(population)):
            competitors_indices = random.sample(range(len(population)), tournament_size)
            winner_index = max(competitors_indices, key=lambda i: fitness_scores[i])
            selected.append(population[winner_index])
        return selected

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, n - 1)
        child1_corrected = parent1[:crossover_point]
        remaining_genes_p2 = [gene for gene in parent2 if gene not in child1_corrected]
        child1_corrected.extend(remaining_genes_p2)

        child2_corrected = parent2[:crossover_point]
        remaining_genes_p1 = [gene for gene in parent1 if gene not in child2_corrected]
        child2_corrected.extend(remaining_genes_p1)

        return child1_corrected, child2_corrected

    def mutate(chromosome, rate):
        if random.random() < rate:
            idx1, idx2 = random.sample(range(n), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    population = initialize_population(population_size, n)
    best_solution = None
    best_fitness = -float('inf')
    generations_without_improvement = 0

    for generation in range(generations):
        fitness_scores = [calculate_fitness(chromo) for chromo in population]
        current_best_idx = fitness_scores.index(max(fitness_scores))

        if fitness_scores[current_best_idx] > best_fitness:
            best_fitness = fitness_scores[current_best_idx]
            best_solution = list(population[current_best_idx])
            generations_without_improvement = 0
            if best_fitness == 0:
                break
        else:
            generations_without_improvement += 1

        if generations_without_improvement >= patience and n > 3:
             break

        selected_population = selection(population, fitness_scores)
        next_population = []
        for i in range(0, population_size, 2):
            if i + 1 < population_size:
                parent1, parent2 = selected_population[i], selected_population[i+1]
                child1, child2 = crossover(parent1, parent2)
                next_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
            else:
                next_population.append(selected_population[i])
        
        population = next_population
        if best_solution and calculate_fitness(best_solution) > calculate_fitness(population[0]):
             idx_to_replace = fitness_scores.index(min(fitness_scores))
             population[idx_to_replace] = best_solution

    end_time = time.time()
    elapsed_time = end_time - start_time
    final_fitness = calculate_fitness(best_solution) if best_solution else -float('inf')

    if final_fitness == 0:
        return best_solution, elapsed_time, 1
    else:
        return best_solution, elapsed_time, 0