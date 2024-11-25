import random
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from math import sqrt, exp

import numpy as np


class Individual:
    def __init__(self, size):
        self.size = size
        self.individual_list = np.random.uniform(-1, 1, size)  # Увеличенный диапазон значений
        self.affinity = 0

    def set_affinity(self, value):
        self.affinity = value

    def mutate(self, mutation_rate):
        for i in range(len(self.individual_list)):
            if random.random() < mutation_rate:
                self.individual_list[i] += random.uniform(-1.0, 1.0)  # Усиленная мутация

    def clone(self):
        return Individual(self.size).from_list(self.individual_list.copy())

    def from_list(self, individual_list):
        self.individual_list = individual_list
        return self


@lru_cache(maxsize=10000)
def euclidean_distance_cached(x, y):
    return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))


def affinity(individual, population):
    distances = [
        euclidean_distance_cached(tuple(individual.individual_list), tuple(p.individual_list))
        for p in population
    ]
    D = min(distances) if distances else float('inf')
    if D == 0:
        D = 1e-10
    return exp(-1 / (D * 10))


def immune_network(
        individual_size,
        population_size,
        iterations,
        clone_count,
        mutation_rate,
        target_accuracy=None
):
    population = [Individual(individual_size) for _ in range(population_size)]
    for ind in population:
        ind.set_affinity(affinity(ind, population))

    for iteration in range(iterations):
        start_iteration = time.time()
        population.sort(key=lambda ind: ind.affinity, reverse=True)
        best_population = population[:clone_count]
        clones = [ind.clone() for ind in best_population for _ in range(clone_count)]

        with ThreadPoolExecutor() as executor:
            mutated_clones = list(executor.map(lambda clone: clone.mutate(mutation_rate) or clone, clones))

        for clone in mutated_clones:
            clone.set_affinity(affinity(clone, population))

        mutated_clones.sort(key=lambda ind: ind.affinity, reverse=True)
        population = population[:population_size // 2] + mutated_clones[:population_size // 2]

        correct_predictions = sum(ind.affinity > 0.5 for ind in population)  # Порог точности 0.5
        accuracy = correct_predictions / population_size
        avg_affinity = sum(ind.affinity for ind in population) / population_size
        print(
            f"Итерация {iteration + 1}: точность {accuracy:.2f}, средняя аффинность {avg_affinity:.4f}, время {time.time() - start_iteration:.2f} секунд.")

        if target_accuracy and accuracy >= target_accuracy:
            print(f"Достигнута желаемая точность: {accuracy:.2f}")
            break

    return population


def save_model(detectors, filepath="model.pkl"):
    import pickle
    with open(filepath, "wb") as f:
        pickle.dump(detectors, f)
    print(f"Модель сохранена в {filepath}")


def load_model(filepath="model.pkl"):
    import pickle
    with open(filepath, "rb") as f:
        detectors = pickle.load(f)
    print(f"Модель загружена из {filepath}")
    return detectors
