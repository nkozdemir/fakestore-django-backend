# Python base image
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-traditional && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (leverage layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

ENV DJANGO_DEBUG=0 \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
    POSTGRES_HOST=db \
    REDIS_URL=redis://redis:6379/1

# Collect static (no static root configured yet, placeholder)
# RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Entrypoint script will handle waiting for db
ENTRYPOINT ["/app/entrypoint.sh"]
