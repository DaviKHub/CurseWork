import re
from collections import defaultdict, Counter
from datetime import datetime


class PreprocessingLogs:
    def __init__(self, log_pattern=None):
        # Регулярное выражение для обработки логов
        self.log_pattern = log_pattern or re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] '
            r'"(?P<method>\S+) (?P<url>\S+) HTTP/\d+\.\d+" (?P<status>\d+) \d+ ".*?" '
            r'"(?P<user_agent>.*?)"'
        )

    def process_log(self, file_path):
        # Data storage
        entries = []
        ip_counter = Counter()
        ip_intervals = defaultdict(list)
        ip_user_agent_changes = Counter()
        ip_status_codes = defaultdict(lambda: {"success": 0, "error": 0})
        skipped_lines = 0
        previous_user_agent = {}

        with open(file_path, "r") as f:
            for line in f:
                match = self.log_pattern.match(line)
                if match:
                    try:
                        # Parse timestamp
                        timestamp_str = match.group("timestamp")
                        timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")

                        # Extract fields
                        ip_address = match.group("ip")
                        status_code = int(match.group("status"))
                        user_agent = match.group("user_agent")

                        # Track User Agent changes
                        if ip_address in previous_user_agent:
                            if previous_user_agent[ip_address] != user_agent:
                                ip_user_agent_changes[ip_address] += 1
                        previous_user_agent[ip_address] = user_agent

                        # Count success/error status codes
                        if 200 <= status_code < 300:
                            ip_status_codes[ip_address]["success"] += 1
                        elif 400 <= status_code < 600:
                            ip_status_codes[ip_address]["error"] += 1

                        # Track entry
                        entries.append({'timestamp': timestamp, 'ip': ip_address})
                        ip_counter[ip_address] += 1
                    except Exception as e:
                        print(f"Ошибка обработки строки: {line.strip()} - {e}")
                else:
                    skipped_lines += 1

        print(f"Пропущено строк: {skipped_lines}")

        # Sort entries by timestamp
        entries.sort(key=lambda x: x['timestamp'])

        # Calculate intervals for each IP
        for i in range(1, len(entries)):
            if entries[i]['ip'] == entries[i - 1]['ip']:
                interval = (entries[i]['timestamp'] - entries[i - 1]['timestamp']).total_seconds()
                ip_intervals[entries[i]['ip']].append(interval)

        # Calculate average interval for each IP
        avg_intervals = {ip: (sum(intervals) / len(intervals)) if intervals else 0 for ip, intervals in
                         ip_intervals.items()}

        # Generate features
        features = []
        for ip, count in ip_counter.items():
            features.append({
                'ip': ip,
                'ip_request_count': count,
                'avg_interval': avg_intervals.get(ip, 0),
                'user_agent_changes': ip_user_agent_changes[ip],
                'success_to_error_ratio': ip_status_codes[ip]["success"] / (ip_status_codes[ip]["error"] + 1) # Avoid division by zero
            })
        return features
