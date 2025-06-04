import random
import time
from utils import is_safe, count_attacking_pairs

def solve_n_queens_backtracking(n):
    solutions = []
    board = [-1] * n

    def backtrack(row):
        if row == n:
            solutions.append(list(board))
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1

    start_time = time.time()
    backtrack(0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return solutions[0] if solutions else None, elapsed_time, len(solutions)

def solve_n_queens_csp(n):
    solutions = []
    assignment = [-1] * n 

    def csp_backtrack_search(row_variable):
        if row_variable == n:
            solutions.append(list(assignment))
            return

        for value_col in range(n):
            if is_safe(assignment, row_variable, value_col):
                assignment[row_variable] = value_col
                csp_backtrack_search(row_variable + 1)
                assignment[row_variable] = -1

    start_time = time.time()
    csp_backtrack_search(0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return solutions[0] if solutions else None, elapsed_time, len(solutions)

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
        crossover_point = random.randint(1, len(parent1) - 1) if len(parent1) > 1 else 0
        
        child1_corrected = parent1[:crossover_point]
        remaining_genes_p2 = [gene for gene in parent2 if gene not in child1_corrected]
        child1_corrected.extend(remaining_genes_p2)
        if len(child1_corrected) != len(parent1):
            seen = set(child1_corrected)
            full_set = list(range(len(parent1)))
            random.shuffle(full_set)
            for gene in full_set:
                if gene not in seen:
                    child1_corrected.append(gene)
            child1_corrected = child1_corrected[:len(parent1)]

        child2_corrected = parent2[:crossover_point]
        remaining_genes_p1 = [gene for gene in parent1 if gene not in child2_corrected]
        child2_corrected.extend(remaining_genes_p1)
        if len(child2_corrected) != len(parent1):
            seen = set(child2_corrected)
            full_set = list(range(len(parent1)))
            random.shuffle(full_set)
            for gene in full_set:
                if gene not in seen:
                    child2_corrected.append(gene)
            child2_corrected = child2_corrected[:len(parent1)]
            
        return child1_corrected, child2_corrected

    def mutate(chromosome, rate):
        if random.random() < rate and len(chromosome) >= 2:
            idx1, idx2 = random.sample(range(len(chromosome)), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    if n == 0 :
        return [], 0, 1
    if n == 1:
        return [0], 0, 1
        
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
        
        if not selected_population: 
            if best_fitness == 0 : break
            else:
                break

        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                parent1, parent2 = selected_population[i], selected_population[i+1]
                child1, child2 = crossover(parent1, parent2)
                next_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
            else:
                next_population.append(selected_population[i])
        
        if not next_population:
            if best_fitness == 0: break
            if population: next_population.extend(population[:population_size - len(next_population)])
            else: next_population = initialize_population(population_size, n)

        population = next_population[:population_size]

        if best_solution:
            if population:
                current_fitness_scores_for_elitism = [calculate_fitness(p) for p in population]
                worst_idx_in_current_pop = current_fitness_scores_for_elitism.index(min(current_fitness_scores_for_elitism))
                if calculate_fitness(best_solution) > current_fitness_scores_for_elitism[worst_idx_in_current_pop]:
                    population[worst_idx_in_current_pop] = list(best_solution)
            else:
                 population.append(list(best_solution))

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    final_fitness = calculate_fitness(best_solution) if best_solution else -float('inf')

    if final_fitness == 0:
        return best_solution, elapsed_time, 1
    else:
        return best_solution, elapsed_time, 0