import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

class ImmuneSystemDetector:
    def __init__(self, threshold=0.8, clone_factor=5, mutation_rate=0.1, generations=10):
        self.detectors = []
        self.threshold = threshold
        self.clone_factor = clone_factor
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.anomalies_detected = defaultdict(int)

    def normalize_data(self, log_entry):
        """Преобразует строку лога в числовой вектор."""
        normalized = [ord(char) % 10 for char in log_entry]
        return np.array(normalized)

    def generate_random_detector(self, data_size):
        """Создает случайный детектор."""
        return np.random.rand(data_size)

    def mutate(self, detector):
        """Мутация детектора."""
        mutation = np.random.rand(len(detector)) < self.mutation_rate
        detector = np.where(mutation, np.random.rand(len(detector)), detector)
        return detector

    def match(self, detector, data):
        """Вычисляет степень совпадения детектора и данных."""
        score = np.dot(detector, data) / (np.linalg.norm(detector) * np.linalg.norm(data))
        return score

    def detect_anomaly(self, data):
        """Проверяет, является ли лог аномалией."""
        for detector in self.detectors:
            if self.match(detector, data) >= self.threshold:
                return True
        return False

    def train(self, normal_data):
        """Тренирует иммунную сеть на нормальных данных."""
        for data in normal_data:
            normalized_data = self.normalize_data(data)
            detector = self.generate_random_detector(len(normalized_data))
            clones = [self.mutate(detector) for _ in range(self.clone_factor)]
            self.detectors.extend(clones)

    def analyze_logs(self, logs):
        """Анализирует логи и подсчитывает аномалии."""
        for generation in range(self.generations):
            anomaly_count = 0
            total_logs = len(logs)

            for log in logs:
                normalized_data = self.normalize_data(log)
                if self.detect_anomaly(normalized_data):
                    anomaly_count += 1

            self.anomalies_detected[generation] = (anomaly_count / total_logs) * 100

    def plot_results(self):
        """Строит график обнаруженных аномалий по поколениям."""
        generations = list(self.anomalies_detected.keys())
        anomalies = list(self.anomalies_detected.values())

        plt.figure(figsize=(10, 6))
        plt.bar(generations, anomalies, color='red', alpha=0.7)
        plt.title('Процент обнаруженных аномалий по поколениям')
        plt.xlabel('Поколение')
        plt.ylabel('Процент обнаруженных атак (%)')
        plt.xticks(generations)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()