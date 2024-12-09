
from datetime import datetime, timedelta
import random

def generate_logs_with_large_ddos(file_path, num_entries, num_attacks):
    """Генерация логов с большим числом уникальных атакующих IP для DDoS."""
    start_time = datetime.now()
    normal_ips = [f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}" for _ in range(100)]
    attack_ips = [f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}" for _ in range(num_attacks)]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)"
    ]
    attack_user_agent = "MaliciousBot/1.0 (DDoS Tool)"
    referers = ["https://example.com", "https://google.com", "https://yahoo.com", "-"]
    resources = ["/index.html", "/api/data", "/login", "/home"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    attack_methods = ["GET", "POST", "OPTIONS"]
    response_codes = [200, 301, 404]
    attack_response_codes = [500, 503]
    response_sizes = [1024, 2048, 512, 0]

    with open(file_path, "w") as f:
        for _ in range(num_entries - num_attacks):
            # Нормальный трафик
            time_stamp = start_time + timedelta(seconds=random.randint(0, 10000))
            formatted_time = time_stamp.strftime("[%d/%b/%Y:%H:%M:%S +0000]")
            ip = random.choice(normal_ips)
            method = random.choice(methods)
            resource = random.choice(resources)
            response_code = random.choice(response_codes)
            response_size = random.choice(response_sizes)
            referer = random.choice(referers)
            user_agent = random.choice(user_agents)
            log_entry = (f'{ip} - - {formatted_time} "{method} {resource} HTTP/1.1" '
                         f'{response_code} {response_size} "{referer}" "{user_agent}"')
            f.write(f"{log_entry}\n")

        for attack_ip in attack_ips:
            # Атакующий трафик
            time_stamp = start_time + timedelta(milliseconds=random.randint(1, 100))
            formatted_time = time_stamp.strftime("[%d/%b/%Y:%H:%M:%S +0000]")
            method = random.choice(attack_methods)
            resource = random.choice(resources)
            response_code = random.choice(attack_response_codes)
            response_size = random.choice([0, 256])  # Маленький размер ответа
            referer = "-"
            log_entry = (f'{attack_ip} - - {formatted_time} "{method} {resource} HTTP/1.1" '
                         f'{response_code} {response_size} "{referer}" "{attack_user_agent}"')
            f.write(f"{log_entry}\n")

    print(f"Файл {file_path} успешно создан с {num_entries} записями, включая {num_attacks} уникальных атакующих IP.")

# Генерация логов
if __name__ == "__main__":
    generate_logs_with_large_ddos("traffic.log", 5000, 1500)