FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port that FastAPI runs on
EXPOSE 8000

# Start FastAPI and explicitly bind to 0.0.0.0
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
