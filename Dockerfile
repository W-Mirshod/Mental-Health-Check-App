FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create data directory
RUN mkdir -p /app/data

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user and set permissions
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Use production-ready server
# Note: Using 1 worker for SQLite compatibility. For production with PostgreSQL, use multiple workers.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
