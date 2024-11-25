import os
import time
from collections import Counter
from colonial_selection import immune_network, save_model


def process_logs(file_path):
    """Обрабатывает лог-файл и формирует признаки."""
    from datetime import datetime
    import re

    entries = []
    ip_counter = Counter()  # Для подсчёта запросов от одного IP

    with open(file_path, "r") as f:
        for line in f:
            match = re.match(r'(\S+ \S+),(\d+) - INFO - (\d+\.\d+\.\d+\.\d+)', line)
            if match:
                timestamp_str = f"{match.group(1)},{match.group(2)}"
                ip_address = match.group(3)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                entries.append({'timestamp': timestamp, 'ip': ip_address})
                ip_counter[ip_address] += 1  # Увеличиваем счётчик запросов

    entries.sort(key=lambda x: x['timestamp'])

    features = []
    for i in range(1, len(entries)):
        # Интервал времени между запросами
        delta = (entries[i]['timestamp'] - entries[i - 1]['timestamp']).total_seconds() * 1000
        interval = min(max(int(delta), 0), 999)

        # Совпадение IP
        ip_match = 1 if entries[i]['ip'] == entries[i - 1]['ip'] else 0

        # Количество запросов от текущего IP
        ip_request_count = ip_counter[entries[i]['ip']]

        features.append([interval, ip_match, ip_request_count])

    return features


def main():
    start_time = time.time()

    individual_size = 3  #признаки
    population_size = 2000  #популяция
    iterations = 50000  #количество итераций
    clone_count = 500  #количество клонов
    mutation_rate = 0.05  #мутация
    target_accuracy = 0.95 #точность

    file_path = "traffic.log"
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден. Сначала создайте файл логов.")
        return

    print("Извлечение признаков из файла traffic.log...")
    start_feature_extraction = time.time()
    features = process_logs(file_path)
    print(f"Извлечение признаков завершено за {time.time() - start_feature_extraction:.2f} секунд.")

    if not features:
        print("Не удалось извлечь признаки из логов. Проверьте содержимое файла.")
        return

    print(f"Извлечено {len(features)} признаков. Обучение иммунной сети...")
    start_training = time.time()
    trained_population = immune_network(
        individual_size=individual_size,
        population_size=population_size,
        iterations=iterations,
        clone_count=clone_count,
        mutation_rate=mutation_rate,
        target_accuracy=target_accuracy
    )
    print(f"Обучение завершено за {time.time() - start_training:.2f} секунд.")

    save_model(trained_population, filepath="ddos_model.pkl")
    print(f"Программа завершена за {time.time() - start_time:.2f} секунд.")


if __name__ == "__main__":
    main()
