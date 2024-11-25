from datetime import datetime, timedelta
import random
from collections import Counter

def generate_traffic_with_attacks(file_path, num_entries, num_attacks):
    """Генерация большого лог-файла с включением атак."""
    start_time = datetime.now()
    ip_addresses = [f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}" for _ in range(100)]
    attack_ips = [f"10.0.0.{random.randint(1, 254)}" for _ in range(10)]  # IP для атак
    ip_counter = Counter()  # Счётчик запросов для IP

    with open(file_path, "w") as f:
        for _ in range(num_entries - num_attacks):
            # Нормальный трафик
            time_stamp = start_time + timedelta(milliseconds=random.randint(1, 5000))
            formatted_time = time_stamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            ip = random.choice(ip_addresses)
            ip_counter[ip] += 1
            method = random.choice(["GET", "POST", "HEAD", "PUT"])
            response_code = random.choice([200, 301])
            log_entry = f"{formatted_time} - INFO - {ip} - {ip_counter[ip]} \"{method} / HTTP/1.1\" {response_code} - 0\n"
            f.write(log_entry)

        for _ in range(num_attacks):
            # Атакующий трафик
            time_stamp = start_time + timedelta(milliseconds=random.randint(1, 100))
            formatted_time = time_stamp.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            ip = random.choice(attack_ips)
            ip_counter[ip] += 1
            method = random.choice(["GET", "POST", "HEAD", "OPTIONS"])  # Необычные методы
            response_code = random.choice([500, 503])
            log_entry = f"{formatted_time} - INFO - {ip} - {ip_counter[ip]} \"{method} / HTTP/1.1\" {response_code} - 1\n"
            f.write(log_entry)

    print(f"Файл {file_path} успешно создан с {num_attacks} атаками и {num_entries - num_attacks} нормальными записями.")
generate_traffic_with_attacks("traffic.log", 500, 30)
