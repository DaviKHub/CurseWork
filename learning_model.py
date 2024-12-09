import time
from concurrent.futures import ThreadPoolExecutor

import colonial_selection
from preprocessing_logs import PreprocessingLogs as PL


def learn_immune_network(
        individual_size: int,
        population_size: int,
        clone_count: int,
        mutation_rate: float,
        target_accuracy: float,
        log_file_path: str,
        model_name: str
):
    start_time = time.time()
    preprocessor = PL()
    print("Извлечение признаков из файла traffic.log...")
    features = preprocessor.process_log(log_file_path)

    if not features:
        print("Не удалось извлечь признаки. Обучение прервано.")
        return

    print(f"Извлечено {len(features)} строк. Обучение иммунной сети...")

    # Инициализация
    immune_network = colonial_selection
    population = [immune_network.Individual(individual_size) for _ in range(population_size)]
    for ind in population:
        ind.set_affinity(immune_network.affinity(ind, population))

    iteration = 0
    accuracies = []  # Список для хранения точности на каждой итерации
    while True:
        population.sort(key=lambda ind: ind.affinity, reverse=True)
        best_population = population[:clone_count]
        clones = [ind.clone() for ind in best_population for _ in range(clone_count)]

        # Мутация
        with ThreadPoolExecutor() as executor:
            mutated_clones = list(executor.map(lambda clone: clone.mutate(mutation_rate) or clone, clones))

        for clone in mutated_clones:
            clone.set_affinity(immune_network.affinity(clone, population))

        mutated_clones.sort(key=lambda ind: ind.affinity, reverse=True)
        population = population[:population_size // 2] + mutated_clones[:population_size // 2]

        # Точность
        accuracy = sum(ind.affinity > 0.6 for ind in population) / population_size
        avg_affinity = sum(ind.affinity for ind in population) / population_size
        accuracies.append(accuracy)  # Сохраняем точность для текущей итерации

        # Возвращаем данные для обновления графика
        yield iteration + 1, accuracy

        print(f"Итерация {iteration + 1}: средняя точность {accuracy:.4f}, средняя аффинность {avg_affinity:.4f}")

        if accuracy >= target_accuracy:
            print(f"Обучение завершено на {iteration + 1} итерации.")
            break

        iteration += 1

    immune_network.save_model(population, filepath=f"{model_name}.pkl")
    print(f"Модель сохранена как {model_name}.pkl")


if __name__ == "__main__":
    for gen, acc in learn_immune_network(
            individual_size=4,  # признаки
            population_size=10,  # популяция
            clone_count=4,  # количество клонов
            mutation_rate=0.01,  # мутация
            target_accuracy=0.95,
            log_file_path="traffic.log",
            model_name="model"
    ):
        print(f"Генерация: {gen}, Точность: {acc}")