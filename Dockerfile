# Dockerfile for Google Cloud Run
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY person_detector.py .
# Create videos directory first
RUN mkdir -p videos

# Copy video files explicitly (both lowercase and uppercase)
COPY City1.mp4 city2.mp4 city3.mp4 city4.mp4 city5.mp4 city6.mp4 city7.mp4 ./videos/

# Create necessary directories
RUN mkdir -p data videos backend/data backend/videos

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV FLASK_APP=backend/app.py

# Expose port (Cloud Run uses PORT env var)
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 300 --chdir backend app:app

