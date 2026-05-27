FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /task_2

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем системные зависимости (для asyncpg)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Python‑зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем портфс
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
