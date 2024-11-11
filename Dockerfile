# Используем официальный образ Python
FROM python:3.9

# Устанавливаем Flask
RUN pip install flask

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с приложением в контейнер
COPY app.py /app

# Запускаем Flask-сервер
CMD ["python", "app.py"]