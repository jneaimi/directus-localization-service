# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install system dependencies and Python requirements
COPY requirements.txt /code/requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /code

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
