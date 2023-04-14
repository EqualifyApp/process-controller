# Use the official Python base image
FROM python:3.9-slim as base

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install required packages
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
