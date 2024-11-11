from log_collector import LogCollector

# if __name__ == "__main__":
#     container_name = "immune_server"
#     log_path = "/app/traffic.log"
#
#     # Инициализация сборщика логов
#     log_collector = LogCollector(container_name, log_path)
#
#     # Сбор логов из Docker-контейнера
#     logs = log_collector.collect_logs_from_docker()
#
#     # Фильтрация релевантных логов
#     filtered_logs = log_collector.filter_relevant_logs(logs)
#     print("Filtered Logs:", filtered_logs)
#
#     # Инициализация иммунной системы
#     immune_system = ImmuneSystemDetector()
#
#     # Тренируем систему на нормальных данных
#     normal_logs = [log for log in filtered_logs if "200" in log]
#     immune_system.train(normal_logs)
#
#     # Анализируем логи для выявления аномалий
#     immune_system.analyze_logs(filtered_logs)
#
#     # Построение графика результатов
#     immune_system.plot_results()

container_name = "immune_server"
log_path = "/app/traffic.log"

# Инициализация сборщика логов
log_collector = LogCollector(container_name, log_path)

# Сбор логов из Docker-контейнера
logs = log_collector.collect_logs_from_docker()

# Фильтрация релевантных логов
filtered_logs = log_collector.filter_relevant_logs(logs)
print("Filtered Logs:", filtered_logs)
