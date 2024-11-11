import logging
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Настройка логирования для приложения
log_handler = logging.FileHandler('traffic.log')
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)

# Настройка логирования для werkzeug (для записи HTTP-запросов)
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.INFO)
werkzeug_log.addHandler(log_handler)

@app.route('/')
def index():
    current_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    app.logger.info(f"Request from {request.remote_addr} to {request.path} at {current_time}")
    return "Hello! This is a simulated server."

@app.route('/login')
def login():
    current_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    app.logger.info(f"Request from {request.remote_addr} to {request.path} at {current_time}")
    return "Login page"

@app.route('/admin')
def admin():
    current_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    app.logger.info(f"Request from {request.remote_addr} to {request.path} at {current_time}")
    return "Admin page"

if __name__ == "__main__":
    # Убедитесь, что Flask слушает все IP-адреса и порт 80
    app.run(host='0.0.0.0', port=80)