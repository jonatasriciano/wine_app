# Use a slim version of the Python 3.9 image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for your application
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Download the wait-for-it script
RUN curl -o /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it

# Copy the requirements file first for better cache utilization
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django application, waiting for the database to be ready, then run migrations and start server
CMD ["wait-for-it", "db:5432", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]