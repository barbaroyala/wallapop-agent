FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 libnss3 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
