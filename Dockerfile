FROM python:3.14-slim

WORKDIR /app

# 1. Сначала копируем только requirements.txt
COPY requirements.txt .

# 2. Устанавливаем зависимости (этот слой будет кэшироваться)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Теперь копируем весь код
COPY . .

# 4. Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]