# Use the official Python base image
FROM python:3.9-slim as base

# Install required packages
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY src /app/src

# Expose the port the app runs on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "src/app.py"]