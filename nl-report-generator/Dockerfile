FROM python:3.11-slim

WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default command to run the backend API
CMD ["python", "app.py"]