import subprocess

class LogCollector:
    def __init__(self, container_name, log_path):
        self.container_name = container_name
        self.log_path = log_path

    def collect_logs_from_docker(self):
        try:
            result = subprocess.run(
                ["docker", "exec", self.container_name, "cat", self.log_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            logs = result.stdout.splitlines()
            return logs
        except subprocess.CalledProcessError as e:
            print(f"Error while fetching logs: {e.stderr}")
            return []