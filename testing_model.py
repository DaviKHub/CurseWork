import pickle
import re
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

def preprocess_data(data, target_size):
    entries = []
    ip_counter = {}

    regex = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\d+)'

    for line in data:
        match = re.match(regex, line)
        if match:
            ip = match.group("ip")
            timestamp = datetime.strptime(match.group("timestamp"), "%d/%b/%Y:%H:%M:%S %z")
            method = match.group("method")
            status = int(match.group("status"))
            size = int(match.group("size"))

            if ip not in ip_counter:
                ip_counter[ip] = 0
            ip_counter[ip] += 1

            entries.append({
                "timestamp": timestamp,
                "ip": ip,
                "status": status,
                "size": size,
                "ip_request_count": ip_counter[ip],
            })

    # Преобразуем в DataFrame
    log_df = pd.DataFrame(entries)

    # Вычисляем временные интервалы между запросами
    log_df["delta_time"] = log_df["timestamp"].diff().dt.total_seconds().fillna(0)

    # Оставляем только числовые столбцы
    X = log_df[["delta_time", "size", "ip_request_count"]]

    # Если числовых признаков меньше, чем нужно, добавляем фиктивные признаки
    if X.shape[1] < target_size:
        for i in range(target_size - X.shape[1]):
            X[f"feature_{i + 1}"] = 0  # Добавляем фиктивные признаки
    elif X.shape[1] > target_size:
        X = X.iloc[:, :target_size]  # Обрезаем лишние признаки

    # Используем частоту IP в качестве метки (пример метки)
    y = log_df["ip_request_count"].apply(lambda x: 1 if x > 10 else 0)  # Простая логика

    return X, y

def load_model(model_path):
    """Загружает обученную модель из файла."""
    print(f"Загрузка модели из {model_path}...")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Модель успешно загружена.")
    return model

def test_model(trained_population, test_data_path, target_size):
    """
    Тестирует обученную популяцию моделей на тестовых данных.
    """
    print(f"Чтение данных из файла {test_data_path}...")
    # Читаем данные из лога как строки
    with open(test_data_path, "r") as f:
        data = f.readlines()

    print("Парсинг данных и создание числовых признаков...")
    # Парсим лог и создаём числовые признаки
    X_test, y_test = preprocess_data(data, target_size)

    # Преобразуем данные для работы с моделью
    X_test = np.array(X_test.values, dtype=float)

    print("Начало тестирования модели...")
    predictions = []
    for individual in trained_population:
        individual_list = np.array(individual.individual_list, dtype=float)

        if individual_list.shape[0] != X_test.shape[1]:
            raise ValueError(
                f"Размерности не совпадают: {individual_list.shape[0]} и {X_test.shape[1]}"
            )

        pred = [1 if np.dot(individual_list, x) > 0 else 0 for x in X_test]
        predictions.append(pred)

    y_pred = np.mean(predictions, axis=0).round()

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Точность модели: {accuracy:.4f}")
    print("Отчет классификации:")
    print(report)

    return accuracy, report

def save_log(log_path, content):
    """Сохраняет результаты в лог-файл."""
    print(f"Сохранение лога в файл {log_path}...")
    with open(log_path, 'a') as log_file:
        log_file.write(content + "\n")
    print("Лог успешно сохранен.")

if __name__ == "__main__":
    model_path = "model.pkl"
    test_data_path = "traffic.log"
    log_path = "test_results.log"
    target_size = 4

    trained_population = load_model(model_path)
    accuracy, report = test_model(trained_population, test_data_path, target_size)
    save_log(log_path, f"Точность: {accuracy:.4f}\n{report}")