FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

    
# Copy project files into the container
COPY . /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set Flask environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 8083

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8083"]
