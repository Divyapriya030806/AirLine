# Use official Python base image
FROM python:3.11-slim

WORKDIR /app

# Copy project (frontend + backend)
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "backend/app.py"]
