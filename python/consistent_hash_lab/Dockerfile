FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set Python path to include the project directory
ENV PYTHONPATH=/app

# Default command
CMD ["bash"]
