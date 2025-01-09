FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/ /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]
