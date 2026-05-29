# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=19191
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory
WORKDIR /app

# Create a non-privileged user to run the app
RUN adduser --disabled-password --gecos "" appuser

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the application directory to the non-privileged user
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user
USER appuser

# Expose the port the app runs on
EXPOSE 19191

# Run the application
CMD ["python", "run.py"]
