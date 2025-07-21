FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8052

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8052", "--server.enableCORS=true"]

