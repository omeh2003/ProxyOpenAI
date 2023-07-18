# Используем официальный образ Python
FROM python:3.9-slim-buster

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы требований
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем исходный код в контейнер
COPY . .

# Запускаем приложение
CMD ["python", "app.py"]
