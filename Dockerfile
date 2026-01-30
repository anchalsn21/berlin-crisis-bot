# Use Python 3.9 base image (compatible with Rasa 3.6.13)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Make app.py executable
RUN chmod +x app.py

# Expose ports
# Port 7860 is the default Hugging Face Spaces port
# Port 5055 is for Rasa actions server
EXPOSE 7860 5055

# Run the app
CMD ["python", "app.py"]

