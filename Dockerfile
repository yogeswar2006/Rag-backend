FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (NOT backend/)
COPY . .

# Temporary build-time env
ENV SECRET_KEY=dummy-build-key
ENV DATABASE_URL=sqlite:///buildtime.db
ENV DEBUG=False

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Start server
CMD sh -c "python manage.py migrate && python manage.py create_admin && daphne config.asgi:application --bind 0.0.0.0 --port ${PORT:-8000}"