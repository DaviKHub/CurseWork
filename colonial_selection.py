import random
from functools import lru_cache
from math import sqrt, exp

import numpy as np


class Individual:
    def __init__(self, size):
        self.size = size
        self.individual_list = np.random.uniform(-1, 1, size)
        self.affinity = 0

    def set_affinity(self, value):
        self.affinity = value

    def mutate(self, mutation_rate):
        for i in range(len(self.individual_list)):
            if random.random() < mutation_rate:
                self.individual_list[i] += random.uniform(-1.0, 1.0)

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
    distance = min(distances) if distances else float('inf')
    if distance == 0:
        distance = 1e-10
    return exp(-1 / (distance * 10))


def save_model(population, filepath="model.pkl"):
    import pickle
    with open(filepath, "wb") as f:
        pickle.dump(population, f)
    print(f"Модель сохранена в {filepath}")

def load_model(filepath="model.pkl"):
    import pickle
    from colonial_selection import Individual  # Убедитесь, что класс импортирован
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    # Проверьте, что загружаются экземпляры класса Individual
    if not all(isinstance(ind, Individual) for ind in model):
        raise ValueError("Некорректный формат данных в модели. Ожидаются экземпляры Individual.")
    return model
