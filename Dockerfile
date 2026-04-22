FROM python:3.11-slim

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Команда для запуска (используем стандартный runserver для учебного проекта)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
